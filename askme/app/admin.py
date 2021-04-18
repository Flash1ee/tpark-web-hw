from django.contrib import admin
from app.models import Author, Question, Answer, Tag, Like

# Register your models here.

admin.site.register(Author)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(Like)
