from django import forms

from .models import *

class BillingForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['full_name', 'email', 'address1', 'address2', 'city', 'state', 'zipcode',]

        exclude = ['user',]

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'address1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 1'}),
            'address2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 2'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}),
        }

        labels = {
            'full_name': 'Full Name',
            'email': 'Email',
            'address1': 'Address 1',
            'address2': 'Address 2',
            'city': 'City',
            'state': 'State',
            'zipcode': 'Zipcode',
        }


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['subscription_type']
