import django.contrib.auth.models
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    avatar = models.ImageField(default=None)

    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

class Tag(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name
    class Tag:
        verbose_name = "Тег"
        verbose_name_plural = 'Теги'



class Like(models.Model):
    count = models.IntegerField(8)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    likes = models.OneToOneField(Like, on_delete=models.CASCADE)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Answer(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    likes = models.OneToOneField(Like, on_delete=models.CASCADE)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

