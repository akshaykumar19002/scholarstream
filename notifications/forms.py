from django import forms
from .models import Announcement
from tinymce.widgets import TinyMCE


class AnnouncementForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 20}))
    class Meta:
        model = Announcement
        fields = ['title', 'content']
