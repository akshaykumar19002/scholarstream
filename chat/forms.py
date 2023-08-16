from django import forms
from tinymce.widgets import TinyMCE

from .models import Email

class EmailForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = Email
        fields = ['subject', 'content',]
    