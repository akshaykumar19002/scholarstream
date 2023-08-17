from django.urls import path
from .views import *

app_name = 'notifications'

urlpatterns = [
    path('', list_notifications, name='list_notifications'),
    path('all/', view_all_notifications, name='view_all_notifications'),
]
