from django.urls import path
from course import views

appname = 'course'

urlpatterns = [
    path('add', views.add_course, name='add'),
    path('', views.list_course, name='list'),
    path('<int:pk>/', views.course_dashboard, name='detail'),
    path('<int:pk>/enroll', views.enroll_course, name='enroll'),
    path('<int:pk>/dropout', views.dropout, name='dropout'),
]