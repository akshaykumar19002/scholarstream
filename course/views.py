from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect

from .forms import CourseForm, ContentForm, LessonForm
from .models import Course, Lesson, Content, Progress
from user.models import UserModel
from cart.cart import Cart

from django.views import View
from django.db import models


@login_required(login_url='user:login')
def add_course(request):
    user = get_object_or_404(get_user_model(), pk=request.user.pk)
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
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'course/dashboard/dashboard.html', {'course': course})


@login_required(login_url='user:login')
def enroll_course(request, pk):
    if request.user.user_type == 'S':
        course = get_object_or_404(Course, pk=pk)
        user = get_object_or_404(get_user_model(), pk=request.user.id)
        user.courses.add(course)
        return redirect('course:list')
    return redirect('course:list')


@login_required(login_url='user:login')
def dropout(request, pk):
    if request.user.user_type == 'S':
        course = get_object_or_404(Course, pk=pk)
        user = get_object_or_404(get_user_model(), pk=request.user.id)
        user.courses.remove(course)
        return redirect('course:list')
    return redirect('course:list')


class AddLesson(LoginRequiredMixin, View):
    
    def get(self, request, course_id):
        user = get_object_or_404(get_user_model(), id=request.user.pk)
        if user.user_type != 'I':
            return redirect('user:forbidden')
        course = get_object_or_404(Course, id=course_id)
        form = LessonForm()
        return render(request, 'course/lesson/add_lesson.html', {'form': form, 'course': course})
    
    def post(self, request, course_id):
        user = get_object_or_404(get_user_model(), id=request.user.pk)
        if user.user_type != 'I':
            return redirect('user:forbidden')
        course = get_object_or_404(Course, id=course_id)
        form = LessonForm(request.POST)
        if form.is_valid():
            new_lesson = Lesson(course=course, title=form.cleaned_data['title'])
            new_lesson.save()
            return redirect('course:detail', pk=course_id)
        else:
            return render(request, 'course/lesson/add_lesson.html', {'form': form, 'course': course})


@login_required(login_url='user:login')
def list_lessons(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    lessons = course.lessons.prefetch_related('contents__viewed_by').all()
    user = get_user_model().objects.get(username=request.user.username)

    lessons_and_contents = []
    for lesson in lessons:
        contents = lesson.contents.all()
        contents_with_viewed_status = [(content, user in content.viewed_by.all()) for content in contents]
        total_contents = len(contents_with_viewed_status)
        completed_contents = sum(viewed for content, viewed in contents_with_viewed_status)
        progress = (completed_contents / total_contents) * 100 if total_contents else 0
        lessons_and_contents.append((lesson, contents_with_viewed_status, progress))

    context = {
        'lessons': lessons_and_contents,
        'course': course
    }
    return render(request, 'course/lesson/list_lessons.html', context)


class AddContent(LoginRequiredMixin, View):
    
    def get(self, request, course_id, lesson_id):
        user = get_object_or_404(get_user_model(), id=request.user.pk)
        if user.user_type != 'I':
            return redirect('user:forbidden')
        form = ContentForm()
        course = get_object_or_404(Course, id=course_id)
        return render(request, 'course/content/add_content.html', {'form': form, 'course': course})
    
    def post(self, request, course_id, lesson_id):
        user = get_object_or_404(get_user_model(), id=request.user.pk)
        if user.user_type != 'I':
            return redirect('user:forbidden')
        course = get_object_or_404(Course, id=course_id)
        lesson = get_object_or_404(Lesson, id=lesson_id)
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
    user = get_object_or_404(get_user_model(), id=request.user.pk)
    content = get_object_or_404(Content, id=content_id)
    content.viewed_by.add(user)
    update_progress(user, content.lesson)
    return render(request, 'course/content/view_content.html', {'content': content})


def update_progress(student, lesson):
    progress, created = Progress.objects.get_or_create(
        student=student,
        lesson=lesson,
        defaults={'is_complete': False}
    )

    # Check if all contents for the lesson are viewed by the student.
    contents_in_lesson = Content.objects.filter(lesson=lesson)
    contents_viewed = [content.viewed_by.filter(id=student.id).exists() for content in contents_in_lesson]

    # If all content has been viewed, mark the lesson as complete.
    if all(contents_viewed):
        progress.is_complete = True
        progress.save()
