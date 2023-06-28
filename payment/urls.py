from django.urls import path
from . import views

urlpatterns = [

    path('checkout/', views.checkout, name='checkout'),
    path('complete-order/', views.complete_order, name='complete-order'),
    path('success/', views.payment_success, name='success'),
    path('failed/', views.payment_failed, name='failed'),
    
    path('subscribe/', views.subscription, name='subscription'),
    path('process_subscription/', views.process_subscription, name='process_subscription'),
    path('subscription_success/', views.subscription_success, name='subscription_success'),
    path('subscription_failed/', views.subscription_failed, name='subscription_failed')

]