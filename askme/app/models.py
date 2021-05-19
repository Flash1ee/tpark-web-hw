from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.utils import timezone


class TagManager(models.Manager):
    def top_tags(self, count=10):
        return self.annotate(count=Count('tag_related')).order_by('-count')[:count]


class AnswerManager(models.Manager):
    def answer_by_question(self, id):
        # return self.annotate(likes=Sum('answer_like__mark')).order_by('-likes').filter(question_id=id)
        return self.annotate(likes=Sum('answer_like__mark')).order_by('pub_date').filter(question_id=id)


class QuestionManager(models.Manager):
    def count_answers(self):
        return self.annotate(answers=Count('answer_related', distinct=True))

    def get_by_likes(self):
        return self.count_answers().order_by('-rating')

    def get_by_id(self, id):
        return self.count_answers().get(id=id)

    def by_tag(self, tag):
        return self.count_answers().filter(tags__name=tag)

    def new(self):
        return self.count_answers().order_by('-pub_date')

    def hot(self):
        return self.get_by_likes()


class ProfileManager(models.Manager):
    def get_top_users(self, count=5):
        return self.annotate(answers=Count('profile_related')).order_by('-answers')[:count]


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name='profile_related')
    avatar = models.ImageField(upload_to="avatar/%Y/%m/%d", default='avatar/200.png')

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Tag(models.Model):
    name = models.CharField(max_length=32)
    objects = TagManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = 'Теги'


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(verbose_name="question_rating", default=0)

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='tag_related')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ['-pub_date']


class Answer(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    correct = models.BooleanField(default=False)
    profile = models.ForeignKey(Profile, related_name='profile_related', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answer_related', on_delete=models.CASCADE)

    objects = AnswerManager()

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
        ordering = ['-pub_date']


class LikeQuestion(models.Model):
    LIKE = '1'
    DISLIKE = '-1'

    MARK = [
        (LIKE, 'Like'),
        (DISLIKE, "Dislike"),
    ]
    mark = models.IntegerField(choices=MARK)
    question = models.ForeignKey(Question, related_name="question_like", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'app_like_question'
        verbose_name = 'Лайк_вопроса'
        verbose_name_plural = 'Лайки_вопросов'


class LikeAnswer(models.Model):
    LIKE = '1'
    DISLIKE = '-1'

    MARK = [
        (LIKE, 'Like'),
        (DISLIKE, "Dislike"),
    ]
    mark = models.IntegerField(choices=MARK)
    answer = models.ForeignKey(Answer, related_name="answer_like", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'app_like_answer'
        verbose_name = 'Лайк_ответа'
        verbose_name_plural = 'Лайки_ответов'
