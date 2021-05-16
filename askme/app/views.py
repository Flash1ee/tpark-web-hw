from django.shortcuts import render, redirect, reverse
from askme.settings import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from app.forms import LoginForm
from django.contrib import auth
from app.models import *
import paginator

users = Profile.objects.get_top_users(count=10)


# Create your views here.
def base_page(request):
    questions = Question.objects.new()
    content = paginator.paginate(questions, request, 10)
    content.update({"category": "Новые вопросы",
                    "forward_category": "Лучшие вопросы",
                    'top_users': users,
                    "key": "authorized",
                    "popular_tags": Tag.objects.top_tags()})
    return render(request, 'index.html', content)


def hot_page(request):
    questions = Question.objects.hot()
    content = paginator.paginate(questions, request, 3)
    content.update({
        "category": "Лучшие вопросы",
        "forward_category": "Новые вопросы",
        "popular_tags": Tag.objects.top_tags(),
        "redirect_new": "new",
        'top_users': users})
    return render(request, 'index.html', content)


def question_page(request, question_id):
    try:
        question = Question.objects.get_by_id(question_id)
        answers = Answer.objects.answer_by_question(question_id)
    except Exception:
        return render(request, 'not_found.html', {"hot_page": "Лучшие вопросы",
                                                  "new_page": "Новые вопросы",
                                                  "popular_tags": Tag.objects.top_tags(),
                                                  'top_users': users
                                                  })

    content = paginator.paginate(answers, request, 3)
    content.update({'question': question,
                    'popular_tags': Tag.objects.top_tags(),
                    'answers': paginator.paginate(answers, request, 3),
                    'top_users': users
                    })
    return render(request, 'question.html', content)


def tag_page(request, tag):
    try:
        tags = Question.objects.by_tag(tag)
    except Exception:
        return render(request, 'not_found.html', {"hot_page": "Лучшие вопросы",
                                                  "new_page": "Новые вопросы",
                                                  "popular_tags": Tag.objects.top_tags(),
                                                  'top_users': users
                                                  })
    content = paginator.paginate(tags, request, 3)
    content.update(
        {'top_users': users,
         'popular_tags': Tag.objects.top_tags(),
         "one_tag": tag})

    return render(request, 'tag.html', content)


@login_required(login_url="login", redirect_field_name=REDIRECT_FIELD_NAME)
def settings(request):
    return render(request, 'settings.html', {'popular_tags': Tag.objects.top_tags(),
                                             'top_users': users})


def login_page(request):
    nxt = request.GET.get(REDIRECT_FIELD_NAME, "new")
    if request.user.is_authenticated:
        return redirect(nxt)

    if request.method == "GET":
        form = LoginForm()
        cache.set(REDIRECT_FIELD_NAME, nxt)
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                next_url = cache.get(REDIRECT_FIELD_NAME)
                cache.delete(REDIRECT_FIELD_NAME)
                return redirect(next_url)
    from pprint import pformat
    print("\n\n", "-" * 100)
    print(f"HERE: {pformat(form)}")
    print("-" * 100, "\n\n")
    return render(request, 'login.html', {'popular_tags': Tag.objects.top_tags(),
                                          'top_users': users,
                                          "form": form})


@login_required(login_url="login", redirect_field_name=REDIRECT_FIELD_NAME)
def logout_view(request):
    auth.logout(request)
    return redirect(reverse("new"))


def signup_page(request):
    return render(request, 'signup.html', {'popular_tags': Tag.objects.top_tags(),
                                           'top_users': users})


@login_required(login_url="login", redirect_field_name=REDIRECT_FIELD_NAME)
def ask_page(request):
    return render(request, 'ask.html',
                  {'popular_tags': Tag.objects.top_tags(),
                   'top_users': users, "key": "authorized"})
