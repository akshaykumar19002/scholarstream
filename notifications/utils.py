from .models import Notification
from django.contrib.auth import get_user_model

def create_notification(user, ctype, message, link=None):
    notification = Notification.objects.create(user=user, content_type=ctype, message=message, link=link)
    notification.save()

def send_notifications_for_all_students(course, ctype, message, link):
    students = get_user_model().objects.filter(courses = course, user_type='S')
    for student in students:
        notification = Notification.objects.create(user=student, content_type=ctype, message=message, link=link)
    