from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Course)
admin.site.register(Content)
admin.site.register(Lesson)
admin.site.register(Progress)
admin.site.register(Assignment)
admin.site.register(AssignmentFile)
admin.site.register(AssignmentSubmission)
admin.site.register(SubmissionFile)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)