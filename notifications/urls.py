from django.urls import path
from .views import *

app_name = 'notifications'

urlpatterns = [
    path('', list_notifications, name='list_notifications'),
    path('all/', view_all_notifications, name='view_all_notifications'),
    
    path('announcement/create/<int:course_id>/', create_announcement, name='create_announcement'),
    path('announcement/all/<int:course_id>/', view_all_announcements, name='view_all_announcements'),
    path('announcement/<int:course_id>/<int:announcement_id>/', view_announcement, name='view_announcement'),
    path('announcement/<int:course_id>/<int:announcement_id>/edit/', edit_announcement, name='edit_announcement'),
    path('announcement/<int:course_id>/<int:announcement_id>/delete/', delete_announcement, name='delete_announcement'),
    
]
