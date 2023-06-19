from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect

from .forms import CourseForm, ContentForm, LessonForm
from .models import Course, Lesson, Content
from user.models import UserModel
from cart.cart import Cart

from django.views import View
from django.db import models


@login_required(login_url='user:login')
def add_course(request):
    user = get_user_model().objects.get(request.user.id)
    if user.user_type != 'I':
        return redirect('forbidden')
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
    return render(request, 'course/dashboard/dashboard.html', {'course': course})


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


class AddLesson(LoginRequiredMixin, View):
    
    def get(self, request, course_id):
        user = get_user_model().objects.get(id=request.user.pk)
        if user.user_type != 'I':
            return redirect('user:forbidden')
        course = Course.objects.get(id=course_id)
        form = LessonForm()
        return render(request, 'course/lesson/add_lesson.html', {'form': form, 'course': course})
    
    def post(self, request, course_id):
        user = get_user_model().objects.get(id=request.user.pk)
        if user.user_type != 'I':
            return redirect('user:forbidden')
        course = Course.objects.get(id=course_id)
        form = LessonForm(request.POST)
        if form.is_valid():
            new_lesson = Lesson(course=course, title=form.cleaned_data['title'])
            new_lesson.save()
            return redirect('course:detail', pk=course_id)
        else:
            return render(request, 'course/lesson/add_lesson.html', {'form': form, 'course': course})


@login_required(login_url='user:login')
def list_lessons(request, course_id):
    course = Course.objects.prefetch_related('lessons__contents').get(pk=course_id)
    lessons = course.lessons.all()

    lessons_and_contents = [(lesson, list(lesson.contents.all())) for lesson in lessons]
    context = {
        'lessons': lessons_and_contents,
        'course': course
    }
    return render(request, 'course/lesson/list_lessons.html', context)


class AddContent(LoginRequiredMixin, View):
    
    def get(self, request, course_id, lesson_id):
        user = get_user_model().objects.get(id=request.user.pk)
        if user.user_type != 'I':
            return redirect('user:forbidden')
        form = ContentForm()
        course = Course.objects.get(id=course_id)
        return render(request, 'course/content/add_content.html', {'form': form, 'course': course})
    
    def post(self, request, course_id, lesson_id):
        user = get_user_model().objects.get(id=request.user.pk)
        if user.user_type != 'I':
            return redirect('user:forbidden')
        course = Course.objects.get(id=course_id)
        lesson = Lesson.objects.get(id=lesson_id)
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            new_content = form.save(commit=False)
            new_content.lesson = lesson
            
            max_order = lesson.contents.aggregate(models.Max('order'))['order__max']
            new_content.order = max_order + 1 if max_order is not None else 0

            new_content.save()
            return redirect('course:detail', pk=course_id)
        else:
            print(form.errors)
            return render(request, 'course/content/add_content.html', {'form': form, 'course': course})


@login_required(login_url='user:login')
def view_content(request, content_id):
    content = Content.objects.get(id=content_id)
    return render(request, 'course/content/view_content.html', {'content': content})
