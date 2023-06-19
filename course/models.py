from django.db import models
import uuid
import os
import mimetypes
from django.utils.deconstruct import deconstructible


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='course-thumbnails/')
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string if instance is not saved yet
            filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        return os.path.join(self.path, filename)

path_and_rename = PathAndRename("contents/")

class Content(models.Model):
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'
    PDF = 'PDF'
    WEBPAGE = 'WEBPAGE'
    AUDIO = 'AUDIO'
    VIDEO = 'VIDEO'

    CONTENT_CHOICES = [
        (TEXT, 'Text'),
        (IMAGE, 'Image'),
        (PDF, 'PDF'),
        (WEBPAGE, 'Webpage'),
        (AUDIO, 'Audio'),
        (VIDEO, 'Video'),
    ]

    title = models.CharField(max_length=200)
    lesson = models.ForeignKey(Lesson, related_name='contents', on_delete=models.CASCADE)
    content_type = models.CharField(
        max_length=10,
        choices=CONTENT_CHOICES,
        default=TEXT,
    )
    order = models.PositiveIntegerField(default=0)
    text_content = models.TextField(blank=True)
    image_content = models.ImageField(upload_to=path_and_rename, blank=True)
    pdf_content = models.FileField(upload_to=path_and_rename, blank=True)
    webpage_content = models.URLField(blank=True)
    audio_content = models.FileField(upload_to=path_and_rename, blank=True)
    audio_type = models.CharField(max_length=100, blank=True)
    video_content = models.FileField(upload_to=path_and_rename, blank=True)
    video_type = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if self.audio_content:
            self.audio_type = mimetypes.guess_type(self.audio_content.name)[0]
        if self.video_content:
            self.video_type = mimetypes.guess_type(self.video_content.name)[0]
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return 'Content for lesson {}'.format(self.lesson.title)
