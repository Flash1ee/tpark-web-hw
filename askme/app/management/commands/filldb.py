from django.core.management.base import BaseCommand
import os
import django
from askme.settings import BASE_DIR
from django.contrib.auth.models import User
from app.models import Question, Profile, LikeQuestion, LikeAnswer, Tag, Answer

from faker import Faker
from collections import OrderedDict
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'askme.settings')
django.setup()

locales = OrderedDict([
    ('en-US', 1),
    ('ru-RU', 2)
])
COUNT_USERS = 10001
COUNT_QUESTIONS = 100001
COUNT_ANSWERS = 1000001
COUNT_TAGS = 10001
LIKES = 2000001

FILE_TAGS = BASE_DIR / 'app/tags.txt'
print(FILE_TAGS)
FILE_QUESTIONS = BASE_DIR / "app/shuffle_q.txt"


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faker = Faker(locales)


    def handle(self, *args, **options):
        self.users_generate(COUNT_USERS)
        self.tags_generate(COUNT_TAGS)
        self.question_generate(COUNT_QUESTIONS)
        self.answers_generate(COUNT_ANSWERS)
        self.like_generate(LIKES)

    def tags_generate(self, count):
        f = open(FILE_TAGS, 'r')
        tags = f.readlines()
        f.close()
        for i in range(count):
            Tag.objects.create(name=tags[random.randint(0, len(tags))][:-1])
        print("TAG_DONE")

    def user_generate(self, i=0):
        username = self.faker.unique.user_name() + str(i % 10)
        first_name = self.faker['ru-RU'].first_name()
        last_name = self.faker['ru-RU'].last_name()
        email = self.faker.email()
        password = self.faker.password()
        user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email,
                                   password=password)
        Profile.objects.create(user=user)

    def users_generate(self, count):
        for i in range(count):
            self.user_generate(i)
        print("USER_DONE")

    def question_generate(self, count):
        f = open(FILE_QUESTIONS, 'r')
        titles = f.readlines()
        f.close()
        cnt_tags = Tag.objects.all().count()
        tag_id = Tag.objects.order_by('id')[0].id
        min_id = Profile.objects.order_by('id')[0].id
        max_id = Profile.objects.order_by('-id')[0].id
        for i in range(count):
            cnt_tags_q = random.randint(1, 5)
            text = self.faker['ru-RU'].paragraph(random.randint(30, 50))
            profile_id = random.randint(min_id, max_id)
            q = Question.objects.create(text=text, title=titles[random.randint(0, len(titles)-1)][:-1],
                                        profile_id=profile_id)

            for j in range(cnt_tags_q):
                tag = Tag.objects.get(id=random.randint(tag_id, tag_id+cnt_tags-1))
                q.tags.add(tag)
        print("QUESTION_DONE")


    def answers_generate(self, count):
        min_profile_id = Profile.objects.order_by('id')[0].id
        max_profile_id = Profile.objects.order_by('-id')[0].id
        min_question_id = Question.objects.order_by('id')[0].id
        max_question_id = Question.objects.order_by('-id')[0].id
        for i in range(count):
            text = self.faker['ru-RU'].paragraph(random.randint(10, 20))
            profile_id = random.randint(min_profile_id, max_profile_id)
            question = random.randint(min_question_id, max_question_id)
            ans = Answer.objects.create(text=text, question_id=question,
                                        profile_id=profile_id)
        print("ANSWERS_DONE")


    def like_generate(self, count):
        min_profile_id = Profile.objects.order_by('id')[0].id
        max_profile_id = Profile.objects.order_by('-id')[0].id
        min_question_id = Question.objects.order_by('id')[0].id
        max_question_id = Question.objects.order_by('-id')[0].id
        for i in range(round(count / 2)):
            while True:
                like = random.randint(0, 1)
                profile_id = random.randint(min_profile_id, max_profile_id)
                question_id = random.randint(min_question_id, max_question_id)
                if like > 0:
                    like = LikeAnswer.LIKE
                else:
                    like = LikeAnswer.DISLIKE
                check = LikeQuestion.objects.filter(question_id=question_id, profile_id=profile_id).count()
                if not check:
                    LikeQuestion.objects.create(question_id=question_id, profile_id=profile_id, mark=like)
                    break
        min_ans_id = Answer.objects.order_by('id')[0].id
        max_ans_id = Answer.objects.order_by('-id')[0].id
        for i in range(round(count / 2)):
            while True:
                like = random.randint(0, 1)
                profile_id = random.randint(min_profile_id, max_profile_id)
                ans_id = random.randint(min_ans_id, max_ans_id)
                if like > 0:
                    like = LikeAnswer.LIKE
                else:
                    like = LikeAnswer.DISLIKE
                check = LikeAnswer.objects. \
                        filter(answer_id=ans_id, profile_id=profile_id).count()
                if not check:
                    LikeAnswer.objects.create(answer_id=ans_id, profile_id=profile_id, mark=like)
                    break
        print("LIKES_DONE")

