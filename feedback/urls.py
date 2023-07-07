from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('<int:course_id>', views.course_reviews, name='review'),
    path('<int:course_id>/add', views.add_review, name='add_review')
]