from django.urls import path
from . import views
from .views import AddContent

appname = 'course'

urlpatterns = [
    path('add', views.add_course, name='add'),
    path('', views.list_course, name='list'),
    path('<int:pk>/', views.course_dashboard, name='detail'),
    path('<int:pk>/enroll', views.enroll_course, name='enroll'),
    path('<int:pk>/dropout', views.dropout, name='dropout'),
    
    path('<int:course_id>/add_lesson/', views.AddLesson.as_view(), name='add_lesson'),
    path('<int:course_id>/lessons/', views.list_lessons, name='list_lessons'),
    path('<int:course_id>/lesson/<int:lesson_id>/add_content/', AddContent.as_view(), name='add_content'),
    path('content/<int:content_id>/', views.view_content, name='view_content'),
    
    path('<int:course_id>/create_assignment/', views.create_assignment, name='create_assignment'),
    path('<int:course_id>/assignments/', views.list_assignments, name='list_assignments'),
    path('<int:course_id>/assignment/<int:assignment_id>/', views.view_assignment, name='view_assignment'),

    path('<int:course_id>/list_quiz/', views.list_quizzes, name='list_quizzes'),
    path('<int:course_id>/quiz/', views.add_quiz, name='create_quiz'),
    path('<int:course_id>/quiz/<int:quiz_id>/', views.view_quiz, name='view_quiz'),
    path('<int:course_id>/delete-quiz/<int:quiz_id>/', views.delete_quiz, name='delete_quiz'),
    path('<int:course_id>/quiz/<int:quiz_id>/publish/', views.publish_quiz, name='publish_quiz'),
    path('<int:course_id>/quiz/<int:quiz_id>/unpublish/', views.hide_quiz, name='hide_quiz'),
    path('<int:course_id>/quiz/<int:quiz_id>/attempt', views.attempt_quiz, name='attempt_quiz'),
    
    path('progress/<int:course_id>/', views.view_course_progress, name='progress'),
    
]