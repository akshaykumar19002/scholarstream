from django.urls import path
from .views import *

app_name = 'chat'

urlpatterns = [
    path('<int:chat_id>/<int:course_id>', chat_room, name='chat_room'),
    path('create_chat_room/<int:course_id>', create_chat_room, name='create_chat_room'),
    path('contact_options/<int:course_id>', contact_options, name='contact_options'),
    path('contact_options/<int:course_id>/<int:student_id>', contact_options, name='contact_options_for_student'),
    path('contact_email/<int:course_id>', contact_email, name='contact_email'),
    path('contact_email/<int:course_id>/<int:student_id>', contact_email, name='contact_email_for_instructor'),

]
