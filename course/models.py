from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='course-thumbnails/')
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name
