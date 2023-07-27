from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserModel
from django import forms
from django.forms.widgets import PasswordInput, TextInput

from payment.models import BillingAddress


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type']

    def __init__(self, *args, **kwargs) -> None:
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['user_type'].required = True

    # email validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        if len(email) > 350:
            raise forms.ValidationError('Email is too long')
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'validate', 'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))
    

class UpdateUsernameForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username']
        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'aria-describedBy': 'usernameHelpBlock'
            }),
        }
        labels = {
            'username': 'Username',
        }
        help_texts = {
            'usernameHelpBlock': 'Enter your new username.',
        }
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UserModel.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        if len(username) > 150:
            raise forms.ValidationError('Username is too long')
        return username


class ChangePasswordForm(forms.Form):
    currentPassword = forms.CharField(label='Current Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current Password',
                'aria-describedBy': 'currentPasswordHelpBlock'}),
        help_text='Enter your current password to confirm your identity.')
    newPassword = forms.CharField(label='New Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'New Password',
                'aria-describedBy': 'newPasswordHelpBlock'}),
        help_text='Enter your new password.')
    confirmPassword = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password',
                'aria-describedBy': 'confirmPasswordHelpBlock'}),
        help_text='Enter your new password again to confirm it.')

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise forms.ValidationError("New password and confirm password must match.")
        return cleaned_data


class AddUpdateAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        exclude = ['user']

        widgets = {
            'email': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address',
                'aria-describedBy': 'emailHelpBlock'
            }),
            'address1': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Address line 1',
                'aria-describedBy': 'address1HelpBlock'
            }),
            'address2': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Address line 2',
                'aria-describedBy': 'address2HelpBlock'
            }),
            'city': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City',
                'aria-describedBy': 'cityHelpBlock'
            }),
            'state': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State',
                'aria-describedBy': 'stateHelpBlock'
            }),
            'zipcode': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Zipcode',
                'aria-describedBy': 'zipcodeHelpBlock'
            }),
        }
        labels = {
            'email': 'Email Address',
            'address1': 'Address Line 1',
            'address2': 'Address Line 2',
            'city': 'City',
            'state': 'State',
            'zipcode': 'Zipcode'
        }
        help_texts = {
            'emailHelpBlock': 'Enter your email address.',
            'address1HelpBlock': 'Enter your address.',
            'address2HelpBlock': 'Enter your address.',
            'cityHelpBlock': 'Enter your city.',
            'stateHelpBlock': 'Enter your state.',
            'zipcodeHelpBlock': 'Enter your zipcode.'
        }
