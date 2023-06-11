from .models import Course
from django.forms import ModelForm, TextInput, EmailInput, CheckboxInput, FileInput


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'is_paid', 'thumbnail']
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
            'is_paid': CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'thumbnail': FileInput(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'name': 'Course Name',
            'description': 'Course Description',
            'is_paid': 'Is this course paid?',
            'thumbnail': 'Course Thumbnail',
        }
        help_texts = {
            'name': 'Enter the name of the course.',
            'description': 'Enter a brief description of the course.',
            'thumbnail': 'Upload a thumbnail for the course.',
        }
