from .models import Course
from django.forms import ModelForm, TextInput, NumberInput, FileInput


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'price', 'thumbnail']
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name',
                'aria-describedBy': 'nameHelpBlock'
            }),
            'description': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter description for the course'
            }),
            'price': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price',
                'aria-describedBy': 'priceHelpBlock'
            }),
            'thumbnail': FileInput(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'name': 'Course Name',
            'description': 'Course Description',
            'is_paid': 'Course Price',
            'thumbnail': 'Course Thumbnail',
        }
        help_texts = {
            'name': 'Enter the name of the course.',
            'description': 'Enter a brief description of the course.',
            'price': 'Enter the price of the course.',
            'thumbnail': 'Upload a thumbnail for the course.',
        }
