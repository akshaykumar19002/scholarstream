from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserModel
from django import forms
from django.forms.widgets import PasswordInput, TextInput


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

    def __init__(self, *args, **kwargs) -> None:
        super(UserRegisterForm, self).__init__(*args, **kwargs)

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
    

class UpdateUserForm(forms.ModelForm):
    password = None

    class Meta:
        model = UserModel

        fields = ['username', 'email']
        exclude = ['password1', 'password2']
    
    def __init__(self, *args, **kwargs) -> None:
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True

    # email validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserModel.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Email already exists')
        if len(email) > 350:
            raise forms.ValidationError('Email is too long')
        return email

    
        