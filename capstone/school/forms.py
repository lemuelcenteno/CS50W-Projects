from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import *


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["role", "username", "email"]


class CourseAddForm(forms.ModelForm):
    code = forms.CharField(label="Course Code", max_length=60)
    title = forms.CharField(label="Course Title", max_length=255)

    class Meta:
        model = Course
        fields = ["code", "title"]
