from django.db import models
from course.models import Course
from django.contrib.auth import get_user_model

# Create your models here.
class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # 1-5 rating

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    date_posted = models.DateTimeField(auto_now_add=True)
    anonymous = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Review by {self.user.username} for {self.course.title}'
