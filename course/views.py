from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q

from .forms import *
from .models import *
from user.models import UserModel
from cart.cart import Cart

from django.views import View
from django.db import models, transaction

from datetime import datetime
from django.utils import timezone

import json
import csv


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
    # return render(request, 'course/dashboard/dashboard.html', {'course': course})
    return redirect('course:list_lessons', course_id=course.id)


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


@login_required(login_url='user:login')
def delete_course(request, pk):
    if request.user.user_type == 'I':
        course = get_object_or_404(Course, pk=pk)
        course.delete()
        return redirect('course:list')
    return redirect('user:forbidden')

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
        'course': course,
        'all_lessons': Lesson.objects.filter(course=course),
        'is_view': False
    }
    return render(request, 'course/lesson/list_lessons.html', context)


@login_required(login_url='user:login')
def view_lesson(request, course_id, lesson_id):
    course = get_object_or_404(Course, pk=course_id)
    lesson = Lesson.objects.prefetch_related('contents__viewed_by').get(pk=lesson_id)
    user = get_user_model().objects.get(username=request.user.username)

    lessons_and_contents = []
    contents = lesson.contents.all()
    contents_with_viewed_status = [(content, user in content.viewed_by.all()) for content in contents]
    total_contents = len(contents_with_viewed_status)
    completed_contents = sum(viewed for content, viewed in contents_with_viewed_status)
    progress = (completed_contents / total_contents) * 100 if total_contents else 0
    lessons_and_contents.append((lesson, contents_with_viewed_status, progress))

    print(lessons_and_contents)

    context = {
        'lessons': lessons_and_contents,
        'all_lessons': Lesson.objects.filter(course=course),
        'course': course,
        'is_view': True
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
    course = content.lesson.course
    content.viewed_by.add(user)
    update_progress(user, content.lesson)
    return render(request, 'course/content/view_content.html', {'content': content, 'course': course})


def update_progress(student, lesson):
    progress, created = LessonProgress.objects.get_or_create(
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
def delete_assignment(request, course_id, assignment_id):
    if request.user.user_type == 'I':
        assignment = get_object_or_404(Assignment, id=assignment_id)
        assignment.delete()
        return redirect('course:list_assignments', course_id=course_id)
    return redirect('user:forbidden')


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
        if request.user.user_type == 'I':
            grade_form = GradeForm(request.POST)
            if grade_form.is_valid():
                submission_id = request.POST.get('submission_id')
                submission = AssignmentSubmission.objects.get(id=submission_id)
                submission.grade = grade_form.cleaned_data['grade']
                submission.grader = request.user
                submission.save()

                return redirect('course:view_assignment', course_id=course.id, assignment_id=assignment.id)
        else:
            form = AssignmentSubmissionForm(request.POST)
            file_form = SubmissionFileForm(request.POST, request.FILES)

            if form.is_valid() and file_form.is_valid():
                submission = form.save(commit=False)
                submission.assignment = assignment
                submission.student = user
                submission.save()

                for f in request.FILES.getlist('file_field'):
                    SubmissionFile.objects.create(file=f, submission=submission)

                AssignmentProgress.objects.update_or_create(assignment=assignment, student=user,
                                                            defaults={'is_complete': False})

                return redirect('course:view_assignment', course_id=course.id, assignment_id=assignment.id)
            else:
                context = {
                    'form': form,
                    'file_form': file_form,
                    'course': course,
                    'assignment': assignment,
                    'submissions': submissions,
                    'current_time': timezone.now(),
                    'grade_form': GradeForm() if request.user.user_type == 'I' else None
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
        'current_time': timezone.now(),
        'grade_form': GradeForm() if request.user.user_type == 'I' else None
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
        data = json.loads(request.body)
        user_id = data.get('user_id')
        quiz_id = data.get('quiz_id')
        answers = data.get('answers')

        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Quiz not found'}, status=404)

        total_score = 0
        ableToScore = True
        response = ''

        for question_id, answer in answers.items():
            question = Question.objects.get(id=question_id)

            if question.question_type == 'MCQ':
                selected_choice = Choice.objects.get(id=answer[0])
                response = selected_choice.choice_text
                if selected_choice.is_correct:
                    total_score += 1

            elif question.question_type == 'MCMS':
                selected_choices = Choice.objects.filter(id__in=answer)
                for choice in selected_choices:
                    response += choice.choice_text + ':'
                if all(choice.is_correct for choice in selected_choices):
                    total_score += 1

            elif question.question_type == 'TF':
                selected_choice = answer[0] == 'True'
                response = answer[0]
                choices = Choice.objects.filter(question=question)
                correct_choice = None
                for choice in choices:
                    if choice.choice_text.lower() == answer[0]:
                        selected_choice = choice
                    if choice.is_correct:
                        correct_choice = choice
                if not correct_choice:
                    ableToScore = False
                elif selected_choice == correct_choice:
                    total_score += 1

            elif question.question_type == 'FITB':
                response = answer[0]
                correct_choice = Choice.objects.filter(question=question, is_correct=True).first()
                if not correct_choice:
                    ableToScore = False
                elif correct_choice.choice_text.lower() == answer[0].lower():
                    total_score += 1

            quiz_attempt = QuizAttempt(
                quiz=quiz,
                user_id=user_id,
                question=question,
                answer_text=response
            )

            quiz_attempt.save()

        quiz_progress = QuizProgress(
            quiz=quiz,
            student_id=user_id,
            is_complete=True,
            total_score=total_score if ableToScore else -1
        )

        quiz_progress.save()

        return JsonResponse({'message': 'Quiz submitted successfully', 'total_score': total_score}, status=200)
    else:
        form = QuizAttemptForm(initial={'quiz': quiz, 'user': user})
        return render(request, 'course/quiz/attempt_quiz.html', {'quiz': quiz, 'questions': questions, 'form': form, 'course': course})


@login_required(login_url='user:login')
def view_attempts(request, course_id, quiz_id):
    course = get_object_or_404(Course, id=course_id)
    student = get_object_or_404(get_user_model(), id=request.user.pk)
    if student.user_type != 'S':
        return redirect('user:forbidden')

    quiz = get_object_or_404(Quiz, course__id=course_id, id=quiz_id)
    attempts = QuizProgress.objects.filter(student=student, quiz=quiz)

    return render(request, 'course/quiz/view_attempts.html', {'quiz': quiz, 'attempts': attempts, 'course': course})


@login_required(login_url='user:login')
def view_course_progress(request, course_id):
    user = get_object_or_404(get_user_model(), id=request.user.pk)
    course = get_object_or_404(Course, id=course_id)
    
    lessons = course.lessons.all()
    for lesson in lessons:
        progress = LessonProgress.objects.filter(lesson=lesson, student=user)
        if len(progress) == 0:
            lesson.progress = None
        else:
            lesson.progress = progress[0]
    
    assignments = course.assignments.all()
    for assignment in assignments:
        progress = AssignmentProgress.objects.filter(assignment=assignment, student=user)
        if len(progress) == 0:
            assignment.progress = None
        else:
            assignment.progress = progress[0]
    
    quizzes = course.quizzes.all()
    for quiz in quizzes:
        progress = QuizProgress.objects.filter(quiz=quiz, student=user)
        if len(progress) == 0:
            quiz.progress = None
        else:
            quiz.progress = progress[0]
    
    course_progress = {
        'course': course,
        'lessons': lessons,
        'assignments': assignments,
        'quizzes': quizzes,
    }

    return render(request, 'course/user_course_progress.html', course_progress)


def course_search(request, search_keyword):
    if request.user.is_authenticated:
        courses = Course.objects.filter(name__icontains = search_keyword, id__in = request.user.courses.all())
        allcourses = Course.objects.all().filter(~Q(id__in = courses), name__icontains = search_keyword)
        coursesInCart = [item['course'].id for item in Cart(request)]
        allcourses = allcourses.exclude(id__in = coursesInCart)
        return render(request, 'course/list_course.html', {'courses': courses, 'allcourses': allcourses})
    allcourses = Course.objects.filter(name__icontains = search_keyword)
    coursesInCart = [item['course'].id for item in Cart(request)]
    allcourses = allcourses.exclude(id__in = coursesInCart)
    return render(request, 'course/list_course.html', {'allcourses': allcourses})


@login_required(login_url='user:login')
def list_grades(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = get_object_or_404(get_user_model(), id=request.user.pk)
    
    if user.user_type == 'S':
        assignments = AssignmentProgress.objects.filter(assignment__course=course, student=user)
        quizzes = QuizProgress.objects.filter(quiz__course=course, student=user)
        otherGrades = OtherGrade.objects.filter(course=course, student=user)
        context = {
            'course': course,
            'assignments': assignments,
            'quizzes': quizzes,
            'otherGrades': otherGrades
        }
        return render(request, 'course/grade/list_grades_student.html', context)
    else:
        if request.method == 'POST':
            if 'assignment_grade_form' in request.POST:
                assignment_grade_form = AssignmentGradeForm(request.POST)
                student_id = request.POST.get('student_id')
                assignment_id = request.POST.get('assignment_id')
                student = get_object_or_404(get_user_model(), id=student_id)
                assignment = get_object_or_404(Assignment, id=assignment_id)
                if assignment_grade_form.is_valid():
                    assignmentProgress = AssignmentProgress.objects.filter(assignment = assignment).first()
                    if assignmentProgress == None:
                        assignmentProgress = AssignmentProgress(assignment = assignment, student = student)
                    assignmentProgress.grade = assignment_grade_form.cleaned_data['grade']
                    assignmentProgress.save()                    
            elif 'quiz_grade_form' in request.POST:
                quiz_grade_form = QuizGradeForm(request.POST)
                student_id = request.POST.get('student_id')
                quiz_id = request.POST.get('quiz_id')
                student = get_object_or_404(get_user_model(), id=student_id)
                quiz = get_object_or_404(Quiz, id=quiz_id)
                if quiz_grade_form.is_valid():
                    quizProgress = QuizProgress.objects.filter(quiz = quiz).first()
                    if quizProgress == None:
                        quizProgress = QuizProgress(quiz = quiz, student = student)
                    quizProgress.total_score = quiz_grade_form.cleaned_data['total_score']
                    quizProgress.save()
                    
        assignments = {}
        quizzes = {}
        otherGrades = {}
        for assignment in Assignment.objects.filter(course = course):
            assignments[assignment] = AssignmentProgress.objects.filter(assignment = assignment)
        for quiz in Quiz.objects.filter(course = course):
            quizzes[quiz] = QuizProgress.objects.filter(quiz = quiz)
            
        oGrades = OtherGrade.objects.filter(course = course)
        for otherGrade in oGrades:
            otherGrades[otherGrade] = OtherGrade.objects.filter(name=otherGrade.name, course = course)
            
        context = {
            'course': course,
            'assignments': assignments,
            'quizzes': quizzes,
            'otherGrades': otherGrades,
            'assignment_grade_form': AssignmentGradeForm(),
            'quiz_grade_form': QuizGradeForm(),
        }
        return render(request, 'course/grade/list_grades_instructor.html', context)


@login_required(login_url='user:login')
def create_extra_grade(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    User = get_user_model()

    if request.method == 'POST':
        form = ExtraGradeForm(request.POST, request.FILES)
        if form.is_valid():
            grade_file = request.FILES.get('grades')
            decoded_file = grade_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            with transaction.atomic():
                for row in reader:
                    student = User.objects.get(pk=int(row['student_id']))
                    grade = OtherGrade(student=student, grade=row['grade'], course=course, 
                                       name=form.cleaned_data['name'], 
                                       description=form.cleaned_data['description'])
                    grade.save()

            return redirect('course:grades', course_id=course.id)
        
    form = ExtraGradeForm()
    return render(request, 'course/grade/create_extra_grade.html', {'course': course, 'form': form})


def download_sample_file(request, course_id):
    User = get_user_model()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sample_grades.csv"'

    writer = csv.writer(response)
    writer.writerow(['student_id', 'grade'])

    students = User.objects.filter(courses__id=course_id)
    for student in students:
        writer.writerow([student.id, ''])

    return response