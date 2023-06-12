from django.urls import path
from . import views

urlpatterns = [

    path('checkout/', views.checkout, name='checkout'),
    path('complete-order/', views.complete_order, name='complete-order'),
    path('success/', views.payment_success, name='success'),
    path('failed/', views.payment_failed, name='failed'),

]