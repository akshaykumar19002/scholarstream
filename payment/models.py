from django.db import models
from django.contrib.auth import get_user_model

from course.models import Course

class BillingAddress(models.Model):
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
    is_paid = models.BooleanField(default=True)
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


SUBSCRIPTION_PRICING = {
    'W': [9.99, 1, 'W', 'Weekly'],
    'BW': [14.99, 2, 'W', 'Bi-Weekly'], 
    'M': [24.99, 1, 'M', 'Monthly'],
    'Q': [69.99, 3, 'M', 'Quarterly'],
    'Y': [249.99, 1, 'Y', 'Yearly']
}


class Subscription(models.Model):
    SUBSCRIPTION_TYPES = [
        ('W', 'Weekly'),
        ('BW', 'Bi-Weekly'),
        ('M', 'Monthly'),
        ('Q', 'Quarterly'),
        ('Y', 'Yearly'),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=2, choices=SUBSCRIPTION_TYPES)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "Subscription for {} - {}".format(self.user, self.subscription_type)
