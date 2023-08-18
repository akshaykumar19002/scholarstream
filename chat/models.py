from django.db import models
from django.conf import settings

class Chat(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='student_chats', on_delete=models.CASCADE)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='instructor_chats', on_delete=models.CASCADE)
    student_online = models.BooleanField(default=False)
    instructor_online = models.BooleanField(default=False)

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}..."

class Email(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_emails', on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_emails', on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} to {self.recipient.username}: {self.content[:50]}..."
