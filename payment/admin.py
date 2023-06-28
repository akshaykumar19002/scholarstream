from django.contrib import admin

from .models import BillingAddress, Order, OrderItem, Subscription

# Register your models here.
admin.site.register(BillingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Subscription)