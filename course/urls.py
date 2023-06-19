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
    path('content/<int:content_id>/', views.view_content, name='view_content')
]