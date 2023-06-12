from django.contrib import admin

from .models import BillingAddress, Order, OrderItem

# Register your models here.
admin.site.register(BillingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
