"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),

    path('subjects/', views.subject_list, name='subjects'),
    path('subjects/add', views.add_subject, name='add_subject'),
    path('subjects/edit/<int:subject_id>', views.edit_subject, name='edit_subject'),
    path('subjects/remove/<int:subject_id>', views.remove_subject, name='remove_subject'),
    path('subjects/details/<int:subject_id>', views.subject_details, name='subject_details'),

    path('students/', views.student_list, name='students'),
    path('students/<int:student_id>', views.enrollment, name='enrollment'),

    path('enrollment/add', views.enroll, name='enroll'),
    path('enrollment/unenroll/<int:enrollment_id>', views.unenroll, name='unenroll'),
    path('enrollment/edit/<int:enrollment_id>', views.edit_enrollment, name='edit_enrollment'),
]
