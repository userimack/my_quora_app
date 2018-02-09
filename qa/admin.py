from django.contrib import admin

# Register your models here.

from qa.models import Question, Answer, Category

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Category)
