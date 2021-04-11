from django.shortcuts import render
import paginator

questions = []
for i in range(0, 11):
    questions.append({
        'id': i,
        'title': 'Title ' + str(i),
        'text': 'Some text for question' + str(i)
    })

answers = []
for i in range(0, 11):
    answers.append({
        'id': i,
        'title': 'Title ' + str(i),
        'text': 'Some text for question' + str(i)
    })
popular_tags = ["MySQL", "Python3", "C++", "Golang", "JavaScript"]

tags = []
for i in range(len(popular_tags)):
    tags.append({
        'tag': popular_tags[i]
    })
popular_users = ["Pupkin", "Bauman", "Straustrup", "Ritchi"]
users = []
for i in range(len(popular_users)):
    users.append({
        'user': popular_users[i]
    })


# Create your views here.


def base_page(request):
    content = paginator.paginate(questions, request, 10)
    content.update({"category": "Новые вопросы", "forward_category": "Лучшие вопросы",
                    "tags": tags, 'users': users,
                    "key": "authorized", "popular_tags":popular_tags})
    return render(request, 'index.html', content)


def hot_page(request):
    content = paginator.paginate(questions, request, 3)
    content.update({"category": "Лучшие вопросы", "forward_category": "Новые вопросы", "questions": questions,
                    "tags": tags, "users": users,
                    "popular_tags": popular_tags, "redirect_new": "new"})
    return render(request, 'index.html', content)


def question_page(request, question_id):
    question = questions[question_id]
    content = paginator.paginate(answers, request, 3)
    content.update({"question": question,"popular_tags":popular_tags, "answers": answers, "tags": tags, "users": users, "one_question": ""})
    return render(request, 'question.html', content)


def tag_page(request, tag):
    tag = {"tag": tag}
    content = paginator.paginate(answers, request, 3)
    content.update(
        {"questions": questions, "answers": answers, "tags": tags, "users": users, "popular_tags": popular_tags,
         "one_tag": tag})

    return render(request, 'tag.html', content)


def settings(request):
    return render(request, 'settings.html', {"key": "authorized", "users": users, "popular_tags": popular_tags})


def login_page(request):
    return render(request, 'login.html', {"tags": tags, "users": users, "popular_tags": popular_tags})


def signup_page(request):
    return render(request, 'signup.html', {"tags": tags, "users": users, "popular_tags": popular_tags})


def ask_page(request):
    return render(request, 'ask.html', {"tags": tags, 'users': users, "key": "authorized", "popular_tags": popular_tags})
