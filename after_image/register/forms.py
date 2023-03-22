from django import forms
from django.contrib.auth.forms import UserCreationForm
from main.models import MyUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = MyUser
        fields = ["username", "email", "password1", "password2"]