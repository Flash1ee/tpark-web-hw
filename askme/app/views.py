from django.shortcuts import render

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
def ask_page(request):
    return render(request, 'ask.html', {"tags": tags, 'users': users, "key": "authorized"})


def base_page(request):
    return render(request, 'index.html',
                  {"category": "Новые вопросы", "forward_category": "Лучшие вопросы", "questions": questions,
                   "tags": tags, 'users': users,
                   "key": "authorized"})


def hot_page(request):
    return render(request, 'index.html',
                  {"category": "Лучшие вопросы", "forward_category": "Новые вопросы", "questions": questions,
                   "tags": tags, "users": users,
                   "popular_tags": popular_tags})


def login_page(request):
    return render(request, 'login.html', {"tags": tags, "users": users})


def signup_page(request):
    return render(request, 'signup.html', {"tags": tags, "users": users})


def question_page(request, question_id):
    question = questions[question_id]
    return render(request, 'question.html', {"question": question, "answers": answers, "tags": tags})


def tag_page(request, tag):
    tag = {"tag": tag}
    return render(request, 'tag.html', {"questions": questions, "answers": answers, "tags": tag})
