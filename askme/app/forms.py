from django import forms
from app.models import Profile, User


class LoginForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'password']

    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-group mb-3"}), label="Логин")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-group mb-3"}), label='Пароль')
