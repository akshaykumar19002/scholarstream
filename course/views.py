from django.shortcuts import render, redirect
from .forms import CourseForm
from .models import Course
import os

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('course:list')  # replace 'courses' with the name of your courses listing page
    else:
        form = CourseForm()

    return render(request, 'course/add_course.html', {'form': form})


def list_course(request):
    courses = Course.objects.all()
    return render(request, 'course/list_course.html', context={'courses': courses})


def course_dashboard(request, pk):
    course = Course.objects.get(pk=pk)
    return render(request, 'course/base_course_dashboard.html', {'course': course})