from .models import Course
from django.forms import ModelForm, TextInput, NumberInput, FileInput
from django import forms
from .models import Content, Lesson
from django.core.exceptions import ValidationError


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


class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = ['title']
        
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'aria-describedBy': 'titleHelpBlock'
            }),
        }
        labels = {
            'title': 'Lesson Title',
        }
        help_texts = {
            'titleHelpBlock': 'Enter the title of the lesson.',
        }
        

def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.mp3', '.wav', '.mp4', '.avi', '.mov', '.flv']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class ContentForm(forms.ModelForm):
    image_content = forms.ImageField(required=False, validators=[validate_file_extension], widget=forms.FileInput(attrs={'accept': 'image/*'}))
    pdf_content = forms.FileField(required=False, validators=[validate_file_extension], widget=forms.FileInput(attrs={'accept': '.pdf'}))
    audio_content = forms.FileField(required=False, validators=[validate_file_extension], widget=forms.FileInput(attrs={'accept': 'audio/*'}))
    video_content = forms.FileField(required=False, validators=[validate_file_extension], widget=forms.FileInput(attrs={'accept': 'video/*'}))

    class Meta:
        model = Content
        fields = ['title', 'content_type', 'text_content', 'image_content', 'pdf_content', 'webpage_content', 'audio_content', 'video_content']
        labels = {
            'title': 'Title',
            'content_type': 'Content Type',
            'text_content': 'Content/Description',
            'image_content': 'Image File',
            'pdf_content': 'PDF File',
            'webpage_content': 'Web URL',
            'audio_content': 'Audio File',
            'video_content': 'Video File',
        }
        help_texts = {
            'title': 'Enter the title of the content',
            'content_type': 'Choose the type of the content',
            'text_content': 'Enter text if content type is Text',
            'image_content': 'Upload image if content type is Image',
            'pdf_content': 'Upload PDF if content type is PDF',
            'webpage_content': 'Enter URL if content type is Webpage',
            'audio_content': 'Upload audio file if content type is Audio',
            'video_content': 'Upload video file if content type is Video',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content_type': forms.Select(attrs={'class': 'form-control'}),
            'text_content': forms.Textarea(attrs={'class': 'form-control'}),
            'image_content': forms.FileInput(attrs={'class': 'form-control'}),
            'pdf_content': forms.FileInput(attrs={'class': 'form-control'}),
            'webpage_content': forms.URLInput(attrs={'class': 'form-control'}),
            'audio_content': forms.FileInput(attrs={'class': 'form-control'}),
            'video_content': forms.FileInput(attrs={'class': 'form-control'}),
        }
