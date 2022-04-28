from django import forms
from django.contrib.auth.models import User

from .models import UserProfile


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["avatar", "name", "phone"]
