from django.contrib import admin

# Register your models here.

from qa.models import Question, Answer, Category


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2


class QuestionAdmin(admin.ModelAdmin):  # version - 2
    fieldsets = [
        (None, {'fields': ['subject']}),
        ('Other Info', {'fields': ['category', 'date']}),
    ]

    inlines = [AnswerInline]

    list_display = ('subject', 'category', 'date')
    list_filter = ['date']

    search_fields = ['subject']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Category)


