from django import forms
from app.models import Profile, Question, Answer, User


class LoginForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'password']

    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-group mb-3"}), label="Логин")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-group mb-3"}), label='Пароль')


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-group mb-3"}), label="Логин")
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-group mb-3"}), label="Email")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-group mb-3"}), label='Пароль')
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-group mb-3"}),
                                      label='Повторите пароль')
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-group mb-3"}), label="Имя")
    avatar = forms.FileField(widget=forms.FileInput(attrs={"class": "form-group mb-3"}), label="Аватар", required=False)

    def clean(self):
        cleaned_data = super().clean()
        passwd_one = cleaned_data['password']
        passwd_two = cleaned_data['password_repeat']
        if passwd_one != passwd_two:
            self.add_error(None, "Пароли не совпадают")


class SettingsForm(forms.ModelForm):
    avatar = forms.FileField(widget=forms.FileInput(attrs={"class": "form-group mb-3"}), label="Аватар", required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'avatar', ]
        labels = {
            "username": "Логин",
            "first_name": "Ник",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-group mb-3", "readonly": "readonly"}),
            "first_name": forms.TextInput(attrs={"class": "form-group mb-3"})
        }
        help_texts = {
            'username': None,
        }

    def save(self, *args, **kwargs):
        user = super().save(*args, *kwargs)
        user.profile_related.avatar = self.cleaned_data['avatar']
        user.profile_related.save()
        return user



class QuestionForm(forms.ModelForm):
    tag_list = forms.CharField(widget=forms.TextInput(attrs={"class": "form-group mb-3",
                                                             "placeholder": "Укажите один или несколько тегов"}),
                               label="Теги")

    class Meta:
        model = Question
        fields = ("title", "text",)
        labels = {
            "title": "Заголовок",
            "text": "Формулировка вопроса",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-group mb-3", "placeholder": "Формулировка вопроса"}),
            "text": forms.Textarea(attrs={"class": "form-group mb-3", "placeholder": "Что такое корутины?"})
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-group mb-3", "placeholder": "Введите ваш ответ"})
        }

