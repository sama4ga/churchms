from django import forms  
from django.contrib.auth.models import User, Group
from .models import Profile  
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError
  
class CustomUserCreationForm(UserCreationForm):  
  first_name = forms.CharField(min_length=2, max_length=150)  
  last_name = forms.CharField(min_length=2, max_length=150)  
  username = forms.CharField(label='Username', min_length=4, max_length=150)  
  email = forms.EmailField(label='Email') 
  password1 = forms.CharField(label='Password', widget=forms.PasswordInput)  
  password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)  
  passport = forms.ImageField(required=False)
  group = forms.ChoiceField(choices=((x.id, x.name) for x in Group.objects.all()))  
  
  def clean_username(self):  
    username = self.cleaned_data['username'].lower()  
    new = User.objects.filter(username = username)  
    if new.count():  
      raise ValidationError("User Already Exist")  
    return username  
  
  def clean_email(self):  
    email = self.cleaned_data['email'].lower()  
    new = User.objects.filter(email=email)  
    if new.count():  
      raise ValidationError(" Email Already Exist")  
    return email  
  
  def clean_password2(self):  
    password1 = self.cleaned_data['password1']  
    password2 = self.cleaned_data['password2']  
  
    if password1 and password2 and password1 != password2:  
      raise ValidationError("Passwords don't match")  
    return password2  
  
  def save(self, commit=True):
    user = User.objects.create_user(  
      username=self.cleaned_data['username'],  
      email=self.cleaned_data['email'],  
      password=self.cleaned_data['password1'],  
      first_name=self.cleaned_data['first_name'],  
      last_name=self.cleaned_data['last_name'] 
    )
    user.groups.clear()
    user.groups.add(self.cleaned_data['group'])
    if self.cleaned_data['passport'] is None:
      profile = Profile(user=user)
    else:
      profile = Profile(user=user, passport=self.cleaned_data['passport'])
    profile.save()
    return user  

class CustomUserUpdateForm(forms.ModelForm):  
  first_name = forms.CharField(min_length=2, max_length=150)  
  last_name = forms.CharField(min_length=2, max_length=150)  
  username = forms.CharField(label='Username', min_length=4, max_length=150)  
  email = forms.EmailField(label='Email')
  group = forms.ChoiceField(choices=((x.id, x.name) for x in Group.objects.all()))  
  
  class Meta:
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'group']
  
  # def save(self, commit=True, *args, **kwargs):  
  #   user = super().save(*args, **kwargs)
  #   user.username=self.cleaned_data['username']
  #   user.email=self.cleaned_data['email']
  #   user.first_name=self.cleaned_data['first_name']
  #   user.last_name=self.cleaned_data['last_name'] 
  #   user.groups.clear()
  #   user.groups.add(self.cleaned_data['group'])
  #   user.save()
  #   return user  

class ProfileForm(forms.ModelForm):
  """Form definition for Profile."""
  # passport = forms.ImageField(required=False)

  class Meta:
    """Meta definition for Profileform."""

    model = Profile
    fields = ('passport',)
