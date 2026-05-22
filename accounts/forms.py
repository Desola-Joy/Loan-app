from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # (we will override below properly)
from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'password1', 'password2']