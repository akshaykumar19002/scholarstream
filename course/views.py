from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings

from .forms import CourseForm
from .models import Course
from user.models import UserModel
from cart.cart import Cart


@login_required(login_url='user:login')
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
    if request.user.is_authenticated:
        courses = Course.objects.filter(id__in = request.user.courses.all())
        allcourses = Course.objects.all().exclude(id__in = courses)
        coursesInCart = [item['course'].id for item in Cart(request)]
        allcourses = allcourses.exclude(id__in = coursesInCart)
        return render(request, 'course/list_course.html', {'courses': courses, 'allcourses': allcourses})
    else:
        allcourses = Course.objects.all()
        coursesInCart = [item['course'].id for item in Cart(request)]
        allcourses = allcourses.exclude(id__in = coursesInCart)
        return render(request, 'course/list_course.html', {'allcourses': allcourses})


@login_required(login_url='user:login')
def course_dashboard(request, pk):
    course = Course.objects.get(pk=pk)
    return render(request, 'course/base_course_dashboard.html', {'course': course})

@login_required(login_url='user:login')
def enroll_course(request, pk):
    if request.user.user_type == 'S':
        course = Course.objects.get(pk=pk)
        user = get_user_model().objects.get(pk=request.user.id)
        user.courses.add(course)
        return redirect('course:list')
    return redirect('course:list')


@login_required(login_url='user:login')
def dropout(request, pk):
    if request.user.user_type == 'S':
        course = Course.objects.get(pk=pk)
        user = get_user_model().objects.get(pk=request.user.id)
        user.courses.remove(course)
        return redirect('course:list')
    return redirect('course:list')

