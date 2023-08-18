from django.db import models
from django.contrib.auth.models import AbstractUser
from course.models import Course


class UserModel(AbstractUser):
    TYPES = [
        ('S', 'Student'),
        ('I', 'Instructor'),
        ('A', 'Admin'),
    ]
    user_type = models.CharField(max_length=2, choices=TYPES, default='S')
    courses = models.ManyToManyField(Course, blank=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User'

    def __str__(self):
        return self.get_full_name() + ' - ' + self.user_type


class BlockedUsers(models.Model):
    student = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='blocked_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='blockers')
