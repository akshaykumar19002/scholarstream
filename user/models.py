from django.db import models
from django.contrib.auth.models import AbstractUser
from course.models import Course


class UserModel(AbstractUser):
    TYPES = [
        ('S', 'Student'),
        ('I', 'Instructor'),
        ('GA', 'Graduate Assistant')
    ]
    user_type = models.CharField(max_length=2, choices=TYPES, default='S')
    courses = models.ManyToManyField(Course, null=True, blank=True)

    class Meta:
        verbose_name = 'User'

    def __str__(self):
        return self.get_full_name() + ' - ' + self.user_type
