from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class MyUser(AbstractUser):
  ROLES = (
    ('MENTOR', 'Mentor'),
    ('STUDENT', 'Student'),
  )

  STATUS = (
    ('NONE', 'None'),
    ('FULL_TIME', 'Full-time'),
    ('PART_TIME', 'Part-time'),
  )

  role = models.CharField(max_length=20, choices=ROLES, default='STUDENT', null=False)
  status = models.CharField(max_length=20, choices=STATUS, default='NONE', null=False)

  def get_student_url(self):
    return f'/students/{self.id}'

  def __str__(self):
    return self.username

class Subject(models.Model):
  OPTIONAL = (
    ('YES', 'Yes'),
    ('NO', 'No'),
  )

  name = models.CharField(max_length=64, null=False)
  code = models.CharField(max_length=16, null=False)
  program = models.TextField(null=False)
  ects = models.IntegerField(null=False)
  semester_full_time = models.IntegerField(null=False)
  semester_part_time = models.IntegerField(null=False)
  optional = models.CharField(max_length=3, choices=OPTIONAL, null=False)

  def get_subject_url(self):
    return f'/subject/{self.id}'

  def __str__(self):
    return self.name

class Enrollment(models.Model):
  student = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
  subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
  status = models.CharField(max_length=64)