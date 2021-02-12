from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class SubjectForm(ModelForm):
  class Meta:
    model = Subject
    fields = ['name', 'code', 'ects', 'semester_full_time', 'semester_part_time', 'optional']

class EnrollmentForm(ModelForm):
  class Meta:
    model = Enrollment
    fields = ['status']

class MyUserForm(UserCreationForm):
  class Meta:
    model = MyUser
    fields = ['username', 'first_name', 'last_name', 'email', 'status', 'password1', 'password2']