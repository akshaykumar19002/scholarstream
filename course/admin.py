from django.contrib import admin
from .models import Course, Content, Lesson, Progress

# Register your models here.
admin.site.register(Course)
admin.site.register(Content)
admin.site.register(Lesson)
admin.site.register(Progress)
