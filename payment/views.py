from django.shortcuts import render
from django.http import JsonResponse

from django.template.loader import render_to_string

from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import BillingAddress, Order, OrderItem
from cart.cart import Cart


def checkout(request):

    if request.user.is_authenticated:
        try:
            shipping_address = BillingAddress.objects.get(user=request.user.id)
            return render(request, 'payment/checkout.html', {'shipping_address': shipping_address})
        except:
            return render(request, 'payment/checkout.html')
    return render(request, 'payment/checkout.html')



@login_required(login_url='user:login')
def complete_order(request):
    
    if request.POST.get('action') == 'post':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        shipping_address = (address1 + '\n' + address2 + '\n' + city + '\n' + state + '\n' + zipcode)

        cart = Cart(request)

        total_cost = cart.get_total_price()

        if request.user.user_type == 'S':
            order = Order(full_name=name, email=email, shipping_address=shipping_address, amount_paid=total_cost, user=request.user)
            order.save()
            print(cart)
            for item in cart:
                print(item)
                order_item = OrderItem(course=item['course'], price=item['price'], order=order, user=request.user)
                order_item.save()
                get_user_model().objects.get(pk=request.user.id).courses.add(item['course'])
            
            user = get_user_model(request.user.id)
            mail_subject = 'Course purchase confirmation'
            mail_body = render_to_string('payment/email-confirmation.html', {
                'user': user.first_name,
            })
            user.email_user(mail_subject, mail_body)

            return JsonResponse({
                'isSuccess': True,
                'message': 'Order completed successfully'
            })

    # return render(request, 'payment/complete-order.html')


@login_required(login_url='user:login')
def payment_success(request):

    for key in list(request.session.keys()):
        if key == 'session-key':
            del request.session[key]

    return render(request, 'payment/payment_success.html')


@login_required(login_url='user:login')
def payment_failed(request):
    return render(request, 'payment/payment_failed.html')
