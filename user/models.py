from django.db import models
from django.contrib.auth.models import User
from course.models import Course


class UserModel(User):
    TYPES = [
        ('S', 'Student'),
        ('I', 'Instructor'),
        ('GA', 'Graduate Assistant')
    ]
    user_type = models.CharField(max_length=2, choices=TYPES, default='S')


class Instructor(UserModel):
    user_type = 'I'
    courses = models.ManyToManyField(Course)

    class Meta:
        verbose_name = 'Instructor'

    def __str__(self):
        return self.get_full_name()


class Student(UserModel):
    user_type = 'S'
    courses = models.ManyToManyField(Course)

    class Meta:
        verbose_name = 'Student'

    def __str__(self):
        return self.get_full_name()
