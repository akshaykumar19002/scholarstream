from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from .models import UserModel as User
from django.views import View
from payment.models import *
from course.models import LessonProgress, AssignmentProgress, QuizProgress

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth import get_user_model

from .forms import *
from .token import user_tokenizer_generate

class Register(View):
    
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'user/registration/register.html', {'form': form})
    
    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'User Verification Email'
            message = render_to_string('user/registration/email-verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': user_tokenizer_generate.make_token(user),
            })
            user.email_user(mail_subject, message)

            return redirect('email-verification-sent')
        return render(request, 'user/registration/register.html', {'form': form})
        

class Login(View):
    
    def get(self, request):
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})
    
    def post(self, request):
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                next_url = request.GET.get('next', reverse('course:list'))
                return HttpResponseRedirect(next_url)
        return render(request, 'user/login.html', {'form': form})

def email_verification(request, uidb64, token):

    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

    if user is not None and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('email-verification-success')
    else:
        return redirect('email-verification-failed')

def email_verification_sent(request):
    return render(request, 'user/registration/email-verification-sent.html')

def email_verification_success(request):
    return render(request, 'user/registration/email-verification-success.html')

def email_verification_failed(request):
    return render(request, 'user/registration/email-verification-failed.html')

def user_logout(request):
    try:
        for key in list(request.session.keys()):
            if key == 'session_key':
                continue
            del request.session[key]
    except KeyError:
        pass

    messages.success(request, 'You have been logged out successfully.')

    return redirect('login')


@login_required(login_url='login')
def delete_user(request):
    user = User.objects.get(id=request.user.id)
    
    if request.method == 'POST':
        user.delete()
        messages.error(request, 'Your user has been deleted successfully.')
        return redirect('course:list')
    
    return render(request, 'user/delete-user.html')


@login_required(login_url='login')
def user_profile(request):
    User = get_user_model()
    user = User.objects.get(id=request.user.id)
    address = BillingAddress.objects.filter(user=user).first()

    username_form = UpdateUsernameForm(request.POST or None, instance=user)
    password_form = ChangePasswordForm(request.POST or None)
    address_form = AddUpdateAddressForm(request.POST or None, address)

    print(request.POST)
    if request.method == 'POST':
        # Update username form
        if 'username_form' in request.POST:
            if username_form.is_valid():
                username_form.save()
            else:
                context = {
                    'username_form': username_form,
                    'password_form': password_form,
                    'address_form': address_form
                }

                return render(request, 'user/profile.html', context)


        # Change password form
        elif 'password_form' in request.POST:
            if password_form.is_valid():
                current_password = password_form.cleaned_data['currentPassword']
                if user.check_password(current_password):
                    new_password = password_form.cleaned_data['newPassword']
                    user.set_password(new_password)
                    user.save()
                    user_logout(request)
                else:
                    password_form.add_error('currentPassword', 'Current password is not correct')
            else:
                context = {
                    'username_form': username_form,
                    'password_form': password_form,
                    'address_form': address_form
                }

                return render(request, 'user/profile.html', context)

        # Add/Update address form
        elif 'address_form' in request.POST:
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = user
                address.save()
            else:
                context = {
                    'username_form': username_form,
                    'password_form': password_form,
                    'address_form': address_form
                }

                return render(request, 'user/profile.html', context)

    context = {
        'username_form': username_form,
        'password_form': password_form,
        'address_form': address_form
    }

    return render(request, 'user/profile.html', context)


def forbidden_error(request):
    return render(request, 'user/forbidden.html')

@login_required(login_url='login')
def user_orders(request):
    user = User.objects.get(id=request.user.id)
    orders = Order.objects.filter(user=user).order_by('-date_ordered')
    return render(request, 'user/dashboard/orders.html', {'orders': orders})

@login_required(login_url='login')
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'user/dashboard/order_detail.html', {'order': order})


@login_required(login_url='login')
def view_user_progress(request):
    user = get_object_or_404(get_user_model(), id=request.user.pk)
    user_courses = user.courses.all()
    progress_data = []
    
    for course in user_courses:
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
                assignment.prog = None
            else:
                assignment.prog = progress[0]
        
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
        progress_data.append(course_progress)

    context = {
        'progress_data': progress_data,
    }
    return render(request, 'user/dashboard/user_progress.html', context)


def email_user(subject, user, template, context):
    mail_subject = subject
    message = render_to_string(template, context)
    user.email_user(mail_subject, message)
    