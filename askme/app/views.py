from django.shortcuts import render
from app.models import *
import paginator

# questions = []
# for i in range(0, 11):
#     questions.append({
#         'id': i,
#         'title': 'Title ' + str(i),
#         'text': 'Some text for question' + str(i)
#     })
#
# answers = []
# for i in range(0, 11):
#     answers.append({
#         'id': i,
#         'title': 'Title ' + str(i),
#         'text': 'Some text for question' + str(i)
#     })
# popular_tags = ["MySQL", "Python3", "C++", "Golang", "JavaScript"]
#
# tags = []
# for i in range(len(popular_tags)):
#     tags.append({
#         'tag': popular_tags[i]
#     })
popular_users = ["Pupkin", "Bauman", "Straustrup", "Ritchi"]
users = []
for i in range(len(popular_users)):
    users.append({
        'user': popular_users[i]
    })


# Create your views here.


def base_page(request):
    questions = Question.objects.new()
    content = paginator.paginate(questions, request, 10)
    content.update({"category": "Новые вопросы", "forward_category": "Лучшие вопросы",
                    'users': users,
                    "key": "authorized", "popular_tags": Tag.objects.top_tags()})
    return render(request, 'index.html', content)


def hot_page(request):
    questions = Question.objects.hot()
    content = paginator.paginate(questions, request, 3)
    content.update({
        "category": "Лучшие вопросы",
        "forward_category": "Новые вопросы",
        "popular_tags": Tag.objects.top_tags(),
        "redirect_new": "new"})
    return render(request, 'index.html', content)


def question_page(request, question_id):
    try:
        question = Question.objects.get_by_id(question_id)
        answers = Answer.objects.answer_by_question(question_id)
    except Exception:
        return render(request, 'not_found.html', {"hot_page": "Лучшие вопросы",
                                                  "new_page": "Новые вопросы",
                                                  "popular_tags": Tag.objects.top_tags()})

    content = paginator.paginate(answers, request, 3)
    content.update({'question': question,
                    'popular_tags': Tag.objects.top_tags(),
                    'answers': paginator.paginate(answers, request, 3),
                    "users": users})
    return render(request, 'question.html', content)


def tag_page(request, tag):
    try:
        tags = Question.objects.by_tag(tag)
    except Exception:
        return render(request, 'not_found.html', {"hot_page": "Лучшие вопросы",
                                                  "new_page": "Новые вопросы",
                                                  "popular_tags": Tag.objects.top_tags()})
    content = paginator.paginate(tags, request, 3)
    content.update(
        {"users": users, "popular_tags": popular_tags,
         "one_tag": tag})

    return render(request, 'tag.html', content)


def settings(request):
    return render(request, 'settings.html', {"key": "authorized", "users": users, "popular_tags": popular_tags})


def login_page(request):
    return render(request, 'login.html', {"tags": tags, "users": users, "popular_tags": popular_tags})


def signup_page(request):
    return render(request, 'signup.html', {"tags": tags, "users": users, "popular_tags": popular_tags})


def ask_page(request):
    return render(request, 'ask.html',
                  {"tags": tags, 'users': users, "key": "authorized", "popular_tags": popular_tags})
