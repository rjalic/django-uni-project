from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import SubjectForm, EnrollmentForm, MyUserForm
from .utils import enough_ects_available, previous_semester_criteria
from .models import *

# Create your views here.
def home(request):
  if not request.user.is_authenticated:
    return redirect('main:login')

  return render(request, 'main/home.html')

def register(request):
  if request.user.is_authenticated:
    return redirect('main/home')

  if request.method == 'POST':
    form = MyUserForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('main:home')
    else:
      for msg in form.error_messages:
        messages.error(request, f'{msg}: {form.error_messages[msg]}')
  
  form = MyUserForm()
  return render(request, 'main/register.html', {'form': form})

def login_request(request):
  if request.user.is_authenticated:
    return redirect('main:home')

  if request.method == 'POST':
    form = AuthenticationForm(request, request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username, password=password)
      if user is not None:
        login(request, user)
        messages.success(request, f'Successfully logged in as {username}')
        return redirect('main:home')
      else:
        messages.error(request, 'Invalid username or password!')
    else:
      messages.error(request, 'Invalid username or password!')
  
  form = AuthenticationForm()
  return render(request, 'main/login.html', {'form': form})

@login_required(login_url='main:login')
def logout_request(request):
  logout(request)
  messages.success(request, 'Logged out successfully.')
  return redirect('main:login')

@login_required(login_url='main:login')
def subject_list(request):
  return render(request, 'main/subject_list.html', {'subjects': Subject.objects.all()})

@login_required(login_url='main:login')
def add_subject(request):
  form = SubjectForm()
  if request.method == 'POST':
    form = SubjectForm(request.POST or None)
    if form.is_valid():
      form.save()
      form = SubjectForm()
      return redirect('main:subjects')

  return render(request, 'main/subject_form.html', {'form': form})

@login_required(login_url='main:login')
def edit_subject(request, subject_id):
  subject = Subject.objects.get(id=subject_id)
  form = SubjectForm(instance=subject)
  if request.method == 'POST':
    form = SubjectForm(request.POST, instance=subject)
    if form.is_valid():
      form.save()
      form = SubjectForm()
      return redirect('main:subjects')
  
  return render(request, 'main/subject_form.html', {'form': form})

@login_required(login_url='main:login')
def remove_subject(request, subject_id):
  subject = Subject.objects.get(id=subject_id)
  subject.delete()
  return redirect('main:subjects')

@login_required(login_url='main:login')
def subject_details(request, subject_id):
  return render(request, 'main/subject_details.html', {'subject': Subject.objects.get(id=subject_id)})

@login_required(login_url='main:login')
def student_list(request):
  return render(request, 'main/student_list.html', {'students': MyUser.objects.filter(role='STUDENT')})

@login_required(login_url='main:login')
def enrollment(request, student_id):
  student = MyUser.objects.get(id=student_id)
  subjects = Subject.objects.all()

  enrollment_info = student.enrollment_set.all()
  enrolled_subjects = enrollment_info.values_list('subject', flat=True)

  num_of_semesters = student.status == 'FULL_TIME' and 7 or 9

  return render(
    request, 
    'main/enrollment.html', 
    {
      'student': student, 
      'subjects': subjects, 
      'enrollment_info': enrollment_info, 
      'range': range(1, num_of_semesters), 
      'enrolled_subjects': enrolled_subjects
    }
  )

@login_required(login_url='main:login')
def enroll(request):
  if request.method == 'POST':
    student_id = request.POST['student_id']
    subject_id = request.POST['subject_id']

    student = MyUser.objects.get(id=student_id)
    subject = Subject.objects.get(id=subject_id)

    selected_status = student.status
    selected_semester = selected_status == 'FULL_TIME' and subject.semester_full_time or subject.semester_part_time

    isEctsValid = enough_ects_available(student, subject, selected_semester)
    if isEctsValid == False:
      messages.error(request, f'Too much ECTS for {selected_semester}. semester!')
      return redirect('main:enrollment', student_id=student_id)

    isPrevEctsValid = previous_semester_criteria(student, subject, selected_semester)
    if isPrevEctsValid == False:
      messages.error(request, 'Not enough points from previous semester')
      return redirect('main:enrollment', student_id=student_id)

    Enrollment.objects.create(student=student, subject=subject, status='enrolled')
    return redirect('main:enrollment', student_id=student_id)

  return render(request, 'main/home.html')

@login_required(login_url='main:login')
def unenroll(request, enrollment_id):
  enrolled_subject = Enrollment.objects.get(id=enrollment_id)
  student_id = enrolled_subject.student.id
  enrolled_subject.delete()
  return redirect('main:enrollment', student_id=student_id)

@login_required(login_url='main:login')
def edit_enrollment(request, enrollment_id):
  enrolled_subject = Enrollment.objects.get(id=enrollment_id)
  student_id = enrolled_subject.student.id
  status_update = enrolled_subject.status == 'enrolled' and 'passed' or 'enrolled'
  enrolled_subject.status = status_update
  enrolled_subject.save()
  return redirect('main:enrollment', student_id=student_id)