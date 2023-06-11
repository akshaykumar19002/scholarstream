from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_paid = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to='course-thumbnails/')

