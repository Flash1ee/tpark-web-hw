from django.db.models import F
from django.shortcuts import render, redirect, reverse
from askme.settings import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.core.cache import cache
from app.forms import LoginForm, RegisterForm, SettingsForm, QuestionForm, AnswerForm
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from app.models import *
import paginator

from pprint import pformat

users = Profile.objects.get_top_users(count=10)


# Create your views here.
def base_page(request):
    if request.is_ajax():
        return like(request)
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
    cache.set(REDIRECT_FIELD_NAME, request.path)
    if request.method == 'POST':
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            ans = form.save(commit=False)
            profile = Profile.objects.get(user=request.user)
            question = Question.objects.get(id=question_id)
            ans.profile = profile
            ans.question = question
            ans.save()
            # answers = Answer.objects.answer_by_question(question_id)
            content = paginator.paginate(Answer.objects.answer_by_question(question_id), request, 3)
            next = f"/question/{question_id}?page={content['pages']}#{ans.id}"
            # cache.set("ans_id", ans.id)
            return redirect("one_question", question_id)
    else:
        try:
            question = Question.objects.get_by_id(question_id)
            answers = Answer.objects.answer_by_question(question_id)
        except Exception:
            return render(request, 'not_found.html', {"hot_page": "Лучшие вопросы",
                                                      "new_page": "Новые вопросы",
                                                      "popular_tags": Tag.objects.top_tags(),
                                                      'top_users': users,
                                                      })
        else:
            form = AnswerForm()
            content = paginator.paginate(answers, request, 3)
            content.update({'question': question,
                            "one_question:": "yes",
                            'popular_tags': Tag.objects.top_tags(),
                            'answers': paginator.paginate(answers, request, 3),
                            'top_users': users,
                            "form": form
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
    if request.method == "GET":
        _profile = Profile.objects.get(user=request.user)
        data = {"username": _profile.user.username, "email": _profile.user.email,
                "first_name": _profile.user.first_name, "avatar": _profile.avatar}
        form = SettingsForm(data)
    else:
        form = SettingsForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse("settings"))
            # User.objects.filter(username=form.cleaned_data['username']).update(email=form.cleaned_data['email'],
            #                                                            first_name=form.cleaned_data['first_name'])
            # Profile.objects.filter(user=request.user).update(avatar=form.cleaned_data['avatar'])

    return render(request, 'settings.html', {'popular_tags': Tag.objects.top_tags(),
                                             'top_users': users, "form": form})


def login_page(request):
    prev = cache.get(REDIRECT_FIELD_NAME)
    nxt = request.GET.get(REDIRECT_FIELD_NAME, prev)
    if not nxt:
        nxt = 'new'
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
            else:
                form.add_error(None, "Пользователь не найден")
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
    prev = cache.get(REDIRECT_FIELD_NAME)
    if not prev:
        prev = "new"
    cache.delete(REDIRECT_FIELD_NAME)
    return redirect(prev)


def signup_page(request):
    if request.method == "GET":
        form = RegisterForm()
    else:
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            try:
                User.objects.get(username=form.cleaned_data['username'], email=form.cleaned_data['email'])
            except User.DoesNotExist:
                form_data = form.cleaned_data.pop("password_repeat")
                form_avatar = form.cleaned_data.pop("avatar")
                user = User.objects.create_user(**form.cleaned_data)
                user.save()
                Profile.objects.create(user=user, avatar=form_avatar)
                return redirect("new")
            else:
                form.add_error(None, "User exist")

    return render(request, 'signup.html', {'popular_tags': Tag.objects.top_tags(),
                                           'top_users': users,
                                           "form": form})


@login_required(login_url="login", redirect_field_name=REDIRECT_FIELD_NAME)
def ask_page(request):
    if request.method == "GET":
        form = QuestionForm()
    else:
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.profile = Profile.objects.get(user=request.user)
            question.save()
            for tag in form.cleaned_data['tag_list'].split():
                new = Tag.objects.get_or_create(name=tag)[0]
                question.tags.add(new)
            question.save()
            return redirect("one_question", question_id=question.id)
        form.save()

    return render(request, 'ask.html',
                  {'popular_tags': Tag.objects.top_tags(),
                   'top_users': users, "key": "authorized", 'form': form})


@require_POST
@login_required()
def like(request):
    data = request.POST

    if data['type'] == 'answer':
        aid = data['aid']
        action = data['action']
        a = Answer.objects.get(id=aid)
        inc = LIKE
        if action == 'dislike':
            inc = DISLIKE
        inc = int(inc)
        a_likes = a.answer_like.filter(profile_id=request.user.profile_related.id).all()

        if (len(a_likes) and a_likes[0].mark == int(inc)):
            return JsonResponse(data, status=400)
        if (len(a_likes)):
            if a_likes[0].mark != inc:
                flag = True
                a_likes[0].mark = inc
                a_likes[0].save()
        else:
            l = LikeAnswer.objects.create(mark=inc, profile=request.user.profile_related, answer=a)
            flag = True
        return JsonResponse(data, status=200)
    else:

        qid = data['qid']
        action = data['action']
        q = Question.objects.get(id=qid)
        inc = LIKE
        if action == 'dislike':
            inc = DISLIKE
        inc = int(inc)
        q_likes = q.question_like.filter(profile_id=request.user.profile_related.id).all()
        if (len(q_likes) and q.question_like.all()[0].mark == int(inc)):
            data.update({"mark": q.question_like.all()[0].mark})
            return JsonResponse(data, status=400)
        if (len(q_likes)):
            if q_likes[0].mark != inc:
                flag = True
                q_likes[0].mark = inc
                q_likes[0].save()
        else:
            l = LikeQuestion.objects.create(mark=inc, profile=request.user.profile_related, question=q)
            flag = True
        if flag:
            if q.rating in [1, -1]:
                inc *= 2
            q.rating = F('rating') + inc
        q.save()
        return JsonResponse(data)


@require_POST
@login_required()
def choice_answer(request):
    data = request.POST
    print(f'HERE: {pformat(data)}')
    if Question.objects.get(id=data['qid']).profile == request.user.profile_related:
        answer = Answer.objects.get(pk=data['aid'])
        answer.correct = not answer.correct
        answer.save()
        print('answer correct status changed')

    return JsonResponse({})
