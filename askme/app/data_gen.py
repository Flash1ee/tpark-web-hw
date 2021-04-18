import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'askme.settings')
django.setup()

from faker import Faker
from collections import OrderedDict
import random

from django.contrib.auth.models import User
from app.models import Question, Author, Like, Tag

locales = OrderedDict([
    ('en-US', 1),
    ('ru-RU', 2)
])
COUNT_USERS = 10000
QUESTIONS = 10 ** 4
LIKES = 2 * 10 ** 6
TAGS = 10000
FILE_TAGS = 'tags.txt'


class Generator:
    def __init__(self):
        self.faker = Faker(locales)

    def tags_generate(self):
        f = open(FILE_TAGS, 'r')
        tags = f.readlines()
        f.close()
        for i in range(TAGS):
            Tag.objects.create(name=tags[random.randint(0, len(tags))][:-2])

    def likes_generate(self):
        for i in range(LIKES):
            Like.objects.create(count=random.randint(-100, 100))

    def user_generate(self):
        username = self.faker.unique.user_name()
        first_name = self.faker['ru-RU'].first_name()
        last_name = self.faker['ru-RU'].last_name()
        email = self.faker.email()
        password = self.faker.password()
        user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email,
                                   password=password)
        Author.objects.create(user=user)

    def users_generate(self):
        for i in range(COUNT_USERS):
            self.user_generate()

    def question_generate(self, count):
        # self.likes_generate()
        # self.tags_generate()
        cnt_authors = Author.objects.all().count()
        f = open('questions.txt', 'r')
        titles = f.readlines()
        f.close()
        cnt_tags = Tag.objects.all().count()
        cnt_likes = Like.objects.all().count()
        for i in range(count):
            cnt_tags_q = random.randint(1, 5)
            text = self.faker['ru-RU'].paragraph(random.randint(100, 200))
            min_id = Author.objects.order_by('id')[0].id
            max_id = Author.objects.order_by('-id')[0].id
            q = Question.objects.create(text=text, title=titles[random.randint(0, len(titles))][:-2],
                                        author_id=random.randint(min_id, max_id),
                                        likes_id=self.faker.unique.random_int(min=1, max=cnt_likes))
            for j in range(cnt_tags_q):
                tag = Tag.objects.get(id=random.randint(1, cnt_tags))
                q.tags.add(tag)


gen = Generator()
# gen.users_generate(COUNT_USERS)
gen.question_generate(QUESTIONS)
