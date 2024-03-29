from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('email_verification/<str:uidb64>/<str:token>', views.email_verification, name='email-verification'),
    path('email_verification_sent/', views.email_verification_sent, name='email-verification-sent'),
    path('email_verification_success/', views.email_verification_success, name='email-verification-success'),
    path('email_verification_failed/', views.email_verification_failed, name='email-verification-failed'),
    
    path('instructor_approval/<str:uidb64>/<str:token>', views.instructor_approval, name='instructor-approval'),
    path('instructor_approval_success/', views.instructor_approval_success, name='instructor-approval-success'),
    path('instructor_approval_failed/', views.instructor_approval_failed, name='instructor-approval-failed'),

    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),

    # path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.user_profile, name='profile'),
    path('delete/', views.delete_user, name='delete'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user/password/password-reset.html'), name='password_reset'),
    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(template_name='user/password/password-reset-sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password/password-reset-form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password/password-reset-complete.html'), name='password_reset_complete'),
    
    path('error_forbidden', views.forbidden_error, name='forbidden'),
    
    path('orders/', views.user_orders, name='orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    
    path('progress/', views.view_user_progress, name='progress'),
    
]