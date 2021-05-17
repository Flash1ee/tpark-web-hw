from django import forms
from app.models import Profile, Question


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
    class Meta:
        model = Profile
        fields = ['username', 'email', 'first_name', 'avatar', ]

    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-group mb-3", "readonly": "readonly"}),
                               label="Логин")
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-group mb-3"}), label="email")
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-group mb-3"}), label="Ник")
    avatar = forms.FileField(widget=forms.FileInput(attrs={"class": "form-group mb-3"}), label="Аватар", required=False)


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
            "title": forms.TextInput(attrs={"placeholder": "Формулировка вопроса"}),
            "text": forms.Textarea(attrs={"placeholder": "Что такое корутины?"})
        }
