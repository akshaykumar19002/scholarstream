from django.db import models
from django.conf import settings
from course.models import Course


class Notification(models.Model):
    EMAIL = 'email'
    ANNOUNCEMENT = 'announcement'
    GRADE = 'grade'
    CHAT = 'chat'
    COURSE_PURCHASE = 'course_purchase'
    COURSE_CONTENT = 'course_content'
    ASSIGNMENT_GRADE = 'assignment_grade'
    EXTRA_GRADES = 'extra_grades'
    CERTIFICATE = 'certificate'
    REGISTRATION = 'registration'
    PASSWORD_CHANGED = 'password_changed'
    USERNAME_CHANGED = 'username_changed'
    CHOICES = [
        (EMAIL, 'Email'),
        (ANNOUNCEMENT, 'Announcement'),
        (GRADE, 'Grade'),
        (CHAT, 'Chat'),
        (COURSE_PURCHASE, 'Course Purchase'),
        (COURSE_CONTENT, 'Course Content'),
        (ASSIGNMENT_GRADE, 'Assignment Graded'),
        (EXTRA_GRADES, 'Extra Grade'),
        (CERTIFICATE, 'Certificate'),
        (REGISTRATION, 'Registration'),
        (PASSWORD_CHANGED, 'Password Changed'),
        (USERNAME_CHANGED, 'Username Changed'),
        
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    content_type = models.CharField(choices=CHOICES, max_length=20)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=200, null=True, blank=True)
    
    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return self.user.username + ":" + self.content_type


class Announcement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='announcements')
