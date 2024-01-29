from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.UserListView.as_view(), name='users-view'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='users-login'),
    path('logout/', views.logout_view, name='users-logout'),
    path('<int:pk>/disable/', views.disable_user, name='users-disable'),
    path('<int:pk>/enable/', views.enable_user, name='users-enable'),
    path('<int:pk>/delete/', views.delete_user, name='users-delete'),
    path('<int:pk>/update/', views.update_user, name='users-update'),
    # path('<int:pk>/update/', views.UserUpdateView.as_view(), name='users-update'),
    path('register/', views.UserRegisterView.as_view(), name='users-register'),
    path('password/change/', auth_views.PasswordChangeView.as_view(
      template_name="users/password_change_form.html", 
      success_url="/users/password/change/done/"
      ), name='users-password-change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(
      template_name="users/password_change_done.html"
      ), name='users-password-change-done'),
    path('password/reset/', auth_views.PasswordResetView.as_view(
      template_name="users/password_reset_form.html", 
      email_template_name="users/password_reset_email_plain.html", 
      # html_email_template_name="users/password_reset_email.html", 
      subject_template_name="users/email_subject.txt", 
      from_email=settings.EMAIL_HOST_USER,
      success_url="/users/password/reset/done/"
      ), name='users-password-reset'),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(
      template_name="users/password_reset_done.html"
      ), name='users-password-reset-done'),
    path('password/reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
      template_name="users/password_reset_confirm_form.html",
      success_url="/users/password/reset/complete/"
      ), name='users-password-reset-confirm'),
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(
      template_name="users/password_reset_complete.html"
      ), name='users-password-reset-complete'),
]