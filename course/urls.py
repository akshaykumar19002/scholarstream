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
    path('<int:pk>/delete', views.delete_course, name='delete'),
    
    path('<int:course_id>/add_lesson/', views.AddLesson.as_view(), name='add_lesson'),
    path('<int:course_id>/lessons/', views.list_lessons, name='list_lessons'),
    path('<int:course_id>/lesson/<int:lesson_id>/', views.view_lesson, name='view_lesson'),
    path('<int:course_id>/lesson/<int:lesson_id>/add_content/', AddContent.as_view(), name='add_content'),
    path('content/<int:content_id>/', views.view_content, name='view_content'),
    path('<int:course_id>/download_content', views.download_course_content, name='download_course_content'),
    path('<int:course_id>/<int:lesson_id>/download_content', views.download_course_content, name='download_lesson_content'),
    
    path('<int:course_id>/create_assignment/', views.create_assignment, name='create_assignment'),
    path('<int:course_id>/assignments/', views.list_assignments, name='list_assignments'),
    path('<int:course_id>/assignment/<int:assignment_id>/', views.view_assignment, name='view_assignment'),
    path('<int:course_id>/assignment/<int:assignment_id>/delete/', views.delete_assignment, name='delete_assignment'),
    path('<int:course_id>/assignment/submission/<int:submission_id>/', views.view_assignment_submission, name='view_submission'),
    path('<int:course_id>/assignment/submission/<int:submission_id>/download', views.download_assignment_submission_content, name='download_submission_content'),

    path('<int:course_id>/list_quiz/', views.list_quizzes, name='list_quizzes'),
    path('<int:course_id>/quiz/', views.add_quiz, name='create_quiz'),
    path('<int:course_id>/quiz/<int:quiz_id>/', views.view_quiz, name='view_quiz'),
    path('<int:course_id>/delete-quiz/<int:quiz_id>/', views.delete_quiz, name='delete_quiz'),
    path('<int:course_id>/quiz/<int:quiz_id>/publish/', views.publish_quiz, name='publish_quiz'),
    path('<int:course_id>/quiz/<int:quiz_id>/unpublish/', views.hide_quiz, name='hide_quiz'),
    path('<int:course_id>/quiz/<int:quiz_id>/attempt', views.attempt_quiz, name='attempt_quiz'),
    path('<int:course_id>/quiz/<int:quiz_id>/view_attempts', views.view_attempts, name='view_attempts'),
    
    path('<int:course_id>/progress/', views.view_course_progress, name='progress'),
    path('<int:course_id>/grades/', views.list_grades, name='grades'),
    path('<int:course_id>/grades/add/', views.create_extra_grade, name='create_extra_grade'),
    path('<int:course_id>/grades/download_sample_file', views.download_sample_file, name='download_sample_file'),
    
    path('search/<str:search_keyword>', views.course_search, name='course_search'),
    
]