from django.contrib import admin
from .models import *

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Content)
admin.site.register(LessonProgress)
admin.site.register(Assignment)
admin.site.register(AssignmentFile)
admin.site.register(AssignmentSubmission)
admin.site.register(SubmissionFile)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(QuizAttempt)
admin.site.register(QuizProgress)
admin.site.register(AssignmentProgress)
