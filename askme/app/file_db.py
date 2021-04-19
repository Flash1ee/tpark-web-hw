import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'askme.settings')
django.setup()

from faker import Faker
from collections import OrderedDict
import random
import datetime

from django.contrib.auth.models import User
from app.models import Question, Profile, LikeQuestion, LikeAnswer, Tag, Answer

locales = OrderedDict([
    ('en-US', 1),
    ('ru-RU', 2)
])
# COUNT_USERS = 1000
# COUNT_QUESTIONS = 5000
# COUNT_ANSWERS = 10000
# COUNT_TAGS = 1000
# LIKES = 5000

COUNT_USERS = 100
COUNT_QUESTIONS = 500
COUNT_ANSWERS = 1000
COUNT_TAGS = 100
LIKES = 500

FILE_TAGS = 'tags.txt'
FILE_QUESTIONS = "questions.txt"


class Generator:
    def __init__(self):
        self.faker = Faker(locales)

    def handler(self):
        self.users_generate(COUNT_USERS)
        self.tags_generate(COUNT_TAGS)
        self.question_generate(COUNT_QUESTIONS)
        self.answers_generate(COUNT_ANSWERS)

    def tags_generate(self, count):
        f = open(FILE_TAGS, 'r')
        tags = f.readlines()
        f.close()
        for i in range(count):
            Tag.objects.create(name=tags[random.randint(0, len(tags))][:-2])

    def user_generate(self):
        username = self.faker.unique.user_name()
        first_name = self.faker['ru-RU'].first_name()
        last_name = self.faker['ru-RU'].last_name()
        email = self.faker.email()
        password = self.faker.password()
        user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email,
                                   password=password)
        Profile.objects.create(user=user)

    def users_generate(self, count):
        for i in range(count):
            self.user_generate()

    def question_generate(self, count):
        f = open('questions.txt', 'r')
        titles = f.readlines()
        f.close()
        cnt_tags = Tag.objects.all().count()
        min_id = Profile.objects.order_by('id')[0].id
        max_id = Profile.objects.order_by('-id')[0].id
        for i in range(count):
            cnt_tags_q = random.randint(1, 5)
            text = self.faker['ru-RU'].paragraph(random.randint(100, 200))
            profile_id = random.randint(min_id, max_id)
            q = Question.objects.create(text=text, title=titles[random.randint(0, len(titles))][:-2],
                                        profile_id=profile_id)

            for j in range(cnt_tags_q):
                tag = Tag.objects.get(id=random.randint(1, cnt_tags))
                q.tags.add(tag)
            like = random.randint(0, 1)
            if like > 0:
                like = LikeQuestion.LIKE
            else:
                like = LikeQuestion.DISLIKE
            LikeQuestion.objects.create(question=q, profile_id=profile_id, mark=like)

    def answers_generate(self, count):
        min_profile_id = Profile.objects.order_by('id')[0].id
        max_profile_id = Profile.objects.order_by('-id')[0].id
        min_question_id = Question.objects.order_by('id')[0].id
        max_question_id = Question.objects.order_by('-id')[0].id
        for i in range(count):
            text = self.faker['ru-RU'].paragraph(random.randint(100, 200))
            profile_id = random.randint(min_profile_id, max_profile_id)
            question = random.randint(min_question_id, max_question_id)
            ans = Answer.objects.create(text=text, question_id=question,
                                        profile_id=profile_id)
            like = random.randint(0, 1)
            if like > 0:
                like = LikeAnswer.LIKE
            else:
                like = LikeAnswer.DISLIKE
            LikeAnswer.objects.create(answer=ans, profile_id=profile_id, mark=like)


gen = Generator()
gen.handler()
