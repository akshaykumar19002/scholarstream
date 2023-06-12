from django.db import models
from django.contrib.auth import get_user_model

from course.models import Course

class BillingAddress(models.Model):
    full_name = models.CharField(max_length=300, blank=False)
    email = models.EmailField(max_length=254, blank=False)
    address1 = models.CharField(max_length=300, blank=False)
    address2 = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=250, blank=False)
    state = models.CharField(max_length=80, null=True, blank=True)
    zipcode = models.CharField(max_length=8, null=True, blank=True)

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Billing Address'

    def __str__(self):
        return 'Billing Address for {}'.format(self.full_name)
    

class Order(models.Model):

    full_name = models.CharField(max_length=300, blank=False)
    email = models.EmailField(max_length=254, blank=False)
    shipping_address = models.TextField(max_length=2000, blank=False)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    date_ordered = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Orders'

    def __str__(self):
        return 'Order #{}'.format(self.id)
    

class OrderItem(models.Model):
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return 'Order #{} - {}'.format(self.order.id, self.course.name)
