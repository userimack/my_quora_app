from django.contrib import admin

# Register your models here.

from qa.models import Question, QuestionRating, Answer, AnswerRating

admin.site.register(Question)
admin.site.register(QuestionRating)
admin.site.register(Answer)
admin.site.register(AnswerRating)
