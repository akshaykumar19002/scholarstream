from django.urls import path
from . import views

app_name = 'certificates'

urlpatterns = [

    path('generate_certificate/<int:course_id>/', views.generate_certificate, name='generate_certificate'),


]
