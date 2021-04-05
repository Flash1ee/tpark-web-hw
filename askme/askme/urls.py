"""askme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.base_page, name="new"),

    path('login/', views.login_page, name="login"),
    path('signup/', views.signup_page, name="signup"),

    path('ask/', views.ask_page, name="ask"),
    path('hot/', views.hot_page, name="hot"),

    path('tag/<str:tag>', views.tag_page, name="tag"),
    path('settings/', views.settings, name="settings"),
    path('question/<int:question_id>', views.question_page, name="one_question"),

]
