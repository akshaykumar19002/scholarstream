from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .cart import Cart
from course.models import Course
from payment.utils import convert_price


def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart/cart-summary.html', {'cart': cart})


def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        course_id = int(request.POST.get('course_id'))
        
        course = get_object_or_404(Course, id=course_id)
        price, currency = convert_price(request, course.currency, course.price)
        cart.add(course, price, currency)

        response = JsonResponse({'isSuccess': True})
        return response
    return JsonResponse({'isSuccess': False})


def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        course_id = int(request.POST.get('course_id'))
        cart.delete(course_id)

        cart_total = cart.get_total_price()

        response = JsonResponse({'isSuccess': True, 'total': cart_total})
        return response
    return JsonResponse({'isSuccess': False})
