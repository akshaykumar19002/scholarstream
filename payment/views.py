from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.gis.geoip2 import GeoIP2

from ipware import get_client_ip
import requests
from decimal import Decimal

from .models import *
from cart.cart import Cart
from .forms import SubscriptionForm, BillingForm
from payment.utils import check_if_user_has_subscription

from paypal.standard.forms import PayPalPaymentsForm

import environ

env = environ.Env()
environ.Env.read_env()

@login_required(login_url='login')
def checkout(request):
    form = BillingForm()
    if request.user.user_type == 'I':
        return redirect('forbidden')
    try:
        shipping_address = BillingAddress.objects.get(user=request.user.id)
        form = BillingForm(shipping_address.__dict__)
        return render(request, 'payment/checkout.html', {'shipping_address': shipping_address, 'has_subscription': check_if_user_has_subscription(request.user), 'form': form})
    except:
        return render(request, 'payment/checkout.html',  {'has_subscription': check_if_user_has_subscription(request.user), 'form': form})


@login_required(login_url='login')
def complete_order(request):
    user = get_user_model().objects.get(pk=request.user.id)
    if request.method == 'POST':
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        
        BillingAddress.objects.filter(user=request.user).delete()
        address = BillingAddress(user=request.user, email=email, address1=address1, address2=address2, city=city, state=state, zipcode=zipcode)
        address.save()

        shipping_address = (address1 + '\n' + address2 + '\n' + city + '\n' + state + '\n' + zipcode)

        cart = Cart(request)

        total_cost = cart.get_total_price()

        if request.user.user_type == 'S':
            try:
                if check_if_user_has_subscription(request.user):
                    order = Order(full_name=user.get_full_name(), email=email, shipping_address=shipping_address, amount_paid=0, user=request.user, is_paid=False)
                else:
                    order = Order(full_name=user.get_full_name(), email=email, shipping_address=shipping_address, amount_paid=total_cost, user=request.user)
                order.save()
                print(cart)
                for item in cart:
                    print(item)
                    order_item = OrderItem(course=item['course'], price=item['price'], order=order, user=request.user)
                    order_item.save()
                    get_user_model().objects.get(pk=request.user.id).courses.add(item['course'])
                
                user = get_user_model().objects.get(id=request.user.id)
                mail_subject = 'Course purchase confirmation'
                mail_body = render_to_string('payment/payment_success_email.html', {
                    'user': user,
                })
                user.email_user(mail_subject, mail_body)
                cart.clear()
                return JsonResponse({'status': 'success', 'message': 'Order placed successfully'})
            except Exception as e:
                print(e)
                return JsonResponse({'status': 'error', 'message': 'Something went wrong'})
        else:
            return JsonResponse({'status': 'error', 'message': 'You are not a student'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Something went wrong'})


@login_required(login_url='login')
def payment_success(request):

    for key in list(request.session.keys()):
        if key == 'session-key':
            del request.session[key]

    return render(request, 'payment/payment_success.html')


@login_required(login_url='login')
def payment_failed(request):
    return render(request, 'payment/payment_failed.html')

def get_currency_code(country_code):
    response = requests.get(f"https://restcountries.com/v2/alpha/{country_code}")
    data = response.json()
    if 'currencies' in data:
        currency = data['currencies'][0]
        return currency['code']
    else:
        return None
    
def get_exchange_rate(base_currency, target_currency):
    OPEN_EXCHANGE_RATES_APP_ID = env('OPEN_EXCHANGE_RATES_APP_ID')
    url = f'https://openexchangerates.org/api/latest.json?app_id={OPEN_EXCHANGE_RATES_APP_ID}&base={base_currency}&symbols={target_currency}'
    response = requests.get(url)
    data = response.json()
    return data['rates'][target_currency]

def get_currency_from_ip(ip_address):
    g = GeoIP2()
    country_code = g.country(ip_address)['country_code']
    currency_code = get_currency_code(country_code)
    return currency_code

def convert_currency(amount, from_currency_code, to_currency_code):
    exchange_rate = get_exchange_rate(from_currency_code, to_currency_code)
    return amount * exchange_rate

def convert(request, amount):
    ip, is_routable = get_client_ip(request)
    currency_code = get_currency_from_ip(ip)
    target_price = convert_currency(amount, 'USD', currency_code)
    target_price = Decimal(target_price).quantize(Decimal('.01'))
    return target_price, currency_code

@login_required(login_url='login')
def subscription(request):
    user = get_user_model().objects.get(pk=request.user.id)
    if request.method == 'POST':
        subscription_plan = request.POST.get('subscription_type')
        currency = request.POST.get('currency')
        price = request.POST.get('price')
    
        request.session['subscription_plan'] = subscription_plan
        request.session['currency'] = currency
        request.session['price'] = price
        return redirect('payment:process_subscription')
    else:
        subs = {}
        for sub, sub_details in SUBSCRIPTION_PRICING.items():
            price, currency = convert(request, sub_details[0])
            print(sub_details[0], price, currency)
            subs[sub] = [price, sub_details[1], sub_details[2], sub_details[3], currency]
        print(subs)
        
        subscription = Subscription.objects.filter(user=user).order_by('-id')
        if len(subscription) > 0:
            subscription = subscription[0]
            subscription.type = SUBSCRIPTION_PRICING[subscription.subscription_type][3]
        else:
            subscription = None
    return render(request, 'payment/subscription/subscription_form.html', {'subs': subs, 'subscription': subscription} )


@login_required(login_url='login')
def process_subscription(request):

    subscription_plan = request.session.get('subscription_plan')
    currency = request.session.get('currency')
    price = request.session.get('price')
    
    host = request.get_host()
    
    subscription_details = SUBSCRIPTION_PRICING[subscription_plan]
    
    user = get_user_model().objects.get(pk=request.user.id)
    
    ## add subscription to database
    subscription = Subscription(user=user, subscription_type=subscription_plan)
    subscription.save()
    
    paypal_dict  = {
        "cmd": "_xclick-subscriptions",
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        "a3": str(price),  # monthly price
        "p3": subscription_details[1],  # duration of each unit (depends on unit)
        "t3": subscription_details[2],  # duration unit ("M for Month")
        "src": "1",  # make payments recur
        "sra": "1",  # reattempt payment on payment error
        "no_note": "1",  # remove extra notes (optional)
        'item_name': 'Scholar Stream subscription',
        'custom': 1,     # custom data, pass something meaningful here
        'currency_code': currency,
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment:subscription_success')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment:subscription_failed')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
    return render(request, 'payment/subscription/process_subscription.html', locals())


@login_required(login_url='login')
def subscription_success(request):
    user = get_user_model().objects.get(pk=request.user.id)
    subscription = Subscription.objects.filter(user=user, is_active=False).order_by('-id')[0]
    subscription.is_active = True
    subscription.save()
    return render(request, 'payment/subscription/subscription_success.html')


@login_required(login_url='login')
def subscription_failed(request):
    return render(request, 'payment/subscription/subscription_failed.html')
