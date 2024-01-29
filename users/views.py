from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, reverse
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group, Permission
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from rest_framework import viewsets
from .serializers import UserSerializer
from .forms import CustomUserCreationForm, CustomUserUpdateForm, ProfileForm

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer

class UserRegisterView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
  form_class = CustomUserCreationForm
  template_name = 'users/register.html'
  success_url = reverse_lazy('users-view')
  permission_required = ["auth.add_user"]
  
  def get_success_message(self, cleaned_data):
    return 'User successfully created'

class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
  form_class = CustomUserUpdateForm
  template_name = 'users/register.html'
  success_url = reverse_lazy('users-view')
  permission_required = ["auth.change_user"]
  
  def get_success_message(self, cleaned_data):
    return 'User successfully updated'

def update_user(request, pk):
  user = get_object_or_404(User, pk=pk)
  profile = user.profile
  if request.method == "POST":
    u_form = CustomUserUpdateForm(request.POST, instance=user)
    p_form = ProfileForm(request.POST, request.FILES, instance=profile)

    if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save()
      messages.success(request, 'User successfully updated')
      return redirect(reverse('users-view'))
  else:
    u_form = CustomUserUpdateForm(instance=user)
    p_form = ProfileForm(instance=profile)

  return render(request, 'users/update_user.html', context={'u_form':u_form, 'p_form':p_form})


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, ListView):
  model = User
  template_name = 'users/user_list.html'
  permission_required = 'auth.view_user'

def logout_view(request):
  logout(request)
  return redirect('users-login')

@login_required()
@permission_required('auth.change_user', raise_exception=True)
def disable_user(request, pk):
  user = get_object_or_404(User, pk=pk)
  user.is_active = False
  user.save()
  return HttpResponse('success')

@login_required()
@permission_required('auth.change_user', raise_exception=True)
def enable_user(request, pk):
  user = get_object_or_404(User, pk=pk)
  user.is_active = True
  user.save()
  return HttpResponse('success')

@login_required()
@user_passes_test(lambda u: u.has_perm('auth.delete_user'))
def delete_user(request, pk):
  user = get_object_or_404(User, pk=pk)
  user.delete()
  return HttpResponse('success')

def send_welcome_email(user):
  from django.conf import settings
  from django.core.mail import send_mail

  subject = "Welcome to churchms"
  message = f"Hi {user.username}, thank you for registering in churchms"
  email_from = settings.EMAIL_HOST_USER
  recipient_list = [user.email,]
  send_mail(subject, message, email_from, recipient_list)

def force_password_reset(user):
  user.set_unusable_password()

def manually_send_reset_password(request, user):
  from django.contrib.auth.forms import PasswordResetForm

  reset_password_form = PasswordResetForm(data={'email':user.email})
  if reset_password_form.is_valid():
    reset_password_form.save(request=request)