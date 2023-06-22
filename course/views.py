from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import *
from .models import *
from user.models import UserModel
from cart.cart import Cart

from django.views import View
from django.db import models

from datetime import datetime
from django.utils import timezone

import json


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


@login_required(login_url='user:login')
def create_assignment(request, course_id):
    user = get_object_or_404(get_user_model(), id=request.user.pk)
    if user.user_type != 'I':
        return redirect('user:forbidden')
    
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        file_form = AssignmentFileForm(request.POST, request.FILES)

        if form.is_valid() and file_form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.creator = request.user
            assignment.save()

            # request.FILES.getlist('file_field') gives a list of all uploaded files
            for f in request.FILES.getlist('file_field'):
                AssignmentFile.objects.create(file=f, assignment=assignment)

            return redirect('course:list_assignments', course_id=course.id)

    else:
        form = AssignmentForm()
        file_form = AssignmentFileForm()

    return render(request, 'course/assignment/add_assignment.html', {'form': form, 'file_form': file_form, 'course': course})


@login_required(login_url='user:login')
def list_assignments(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    assignments = Assignment.objects.filter(course=course)

    context = {
        'course': course,
        'assignments': assignments
    }
    return render(request, 'course/assignment/list_assignments.html', context)


@login_required(login_url='user:login')
def view_assignment(request, course_id, assignment_id):
    user = get_object_or_404(get_user_model(), id=request.user.pk)
    
    course = get_object_or_404(Course, id=course_id)
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.user.user_type == 'S':
        submissions = AssignmentSubmission.objects.filter(assignment=assignment, student=user)
    else:
        submissions = AssignmentSubmission.objects.filter(assignment=assignment)
        
    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST)
        file_form = SubmissionFileForm(request.POST, request.FILES)

        if form.is_valid() and file_form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = user
            submission.save()

            for f in request.FILES.getlist('file_field'):
                SubmissionFile.objects.create(file=f, submission= submission)

            return redirect('course:view_assignment', course_id=course.id, assignment_id=assignment.id)
        else:
            context = {
                'form': form,
                'file_form': file_form,
                'course': course,
                'assignment': assignment,
                'submissions': submissions,
                'current_time': timezone.now()
            }
            return render(request, 'course/assignment/view_assignment.html', context)
    else:
        form = AssignmentSubmissionForm()
        file_form = SubmissionFileForm()

    context = {
        'form': form,
        'file_form': file_form,
        'course': course,
        'assignment': assignment,
        'submissions': submissions,
        'current_time': timezone.now()
    }
    return render(request, 'course/assignment/view_assignment.html', context)


@login_required(login_url='user:login')
def list_quizzes(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if (request.user.user_type != 'I'):
        quizzes = Quiz.objects.filter(course=course, is_published=True)
    else:
        quizzes = Quiz.objects.filter(course=course)
    return render(request, 'course/quiz/list_quizzes.html', {'course': course, 'quizzes': quizzes})


@login_required(login_url='user:login')
def add_quiz(request, course_id):
    if (request.user.user_type != 'I'):
        return redirect('user:forbidden')
    course = get_object_or_404(Course, id=course_id)
    user = get_object_or_404(get_user_model(), id=request.user.pk)
    if request.method == 'POST':
        data = json.loads(request.body)
        quiz = Quiz.objects.update_or_create(
            course_id=course_id,
            creator=user,
            name=data.get('quizName'),
            description=data.get('quizDescription'),
            attempts_allowed=int(data.get('attemptsAllowed')),
            due_date=datetime.strptime(data.get('dueDate'), '%Y-%m-%dT%H:%M')
        )
        questions = data.get('questions', [])
        quiz = quiz[0]
        for question_data in questions:
            question = Question.objects.update_or_create(
                quiz=quiz,
                question_text=question_data.get('text'),
                question_type=question_data.get('type'),
            )
            question = question[0]
            choices = question_data.get('choices', [])
            for choice_data in choices:
                Choice.objects.update_or_create(
                    question=question,
                    choice_text=choice_data.get('text'),
                    is_correct=choice_data.get('isCorrect'),
                )
        return JsonResponse({'success': True})
    else:
        return render(request, 'course/quiz/add_quiz.html', {'course': course})


@login_required(login_url='user:login')
def view_quiz(request, course_id, quiz_id):
    if (request.user.user_type != 'I'):
        return redirect('user:forbidden')
    course = get_object_or_404(Course, id=course_id)
    quiz = get_object_or_404(Quiz, course__id=course_id, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'course/quiz/view_quiz.html', {'quiz': quiz, 'questions': questions, 'course': course})


@login_required(login_url='user:login')
def delete_quiz(request, course_id, quiz_id):
    if (request.user.user_type != 'I'):
        return redirect('user:forbidden')
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.delete()
    return redirect('course:list_quizzes', course_id=course_id)

@login_required(login_url='user:login')
def publish_quiz(request, course_id, quiz_id):
    if (request.user.user_type != 'I'):
        return redirect('user:forbidden')
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.is_published = True
    quiz.save()
    return redirect('course:list_quizzes', course_id=course_id)

@login_required(login_url='user:login')
def hide_quiz(request, course_id, quiz_id):
    if (request.user.user_type != 'I'):
        return redirect('user:forbidden')
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.is_published = False
    quiz.save()
    return redirect('course:list_quizzes', course_id=course_id)


@login_required(login_url='user:login')
def attempt_quiz(request, course_id, quiz_id):
    course = get_object_or_404(Course, id=course_id)
    user = get_object_or_404(get_user_model(), id=request.user.pk)
    quiz = get_object_or_404(Quiz, course__id=course_id, id=quiz_id)
    questions = quiz.questions.all()
    
    if user.user_type != 'S':
        return redirect('user:forbidden')

    if request.method == 'POST':
        form = QuizAttemptForm(request.POST)
        if form.is_valid():
            question_id = form.cleaned_data.get('question').id
            attempts = QuizAttempt.objects.filter(user=user, quiz=quiz, question__id=question_id).count()

            if attempts <= quiz.attempts_allowed:
                form.save()  
                return redirect('course:list_quizzes', course_id=course_id)
            return redirect('course:list_quizzes', course_id=course_id)
        else:
            print(form.errors)
            return render(request, 'course/quiz/attempt_quiz.html', {'quiz': quiz, 'questions': questions, 'form': form, 'course': course})
    else:
        form = QuizAttemptForm(initial={'quiz': quiz, 'user': user})
        return render(request, 'course/quiz/attempt_quiz.html', {'quiz': quiz, 'questions': questions, 'form': form, 'course': course})
