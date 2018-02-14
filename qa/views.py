#  from django.shortcuts import render
from django.views import generic
from .models import Question
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class IndexView(generic.ListView):
    model = Question
    template_name = 'qa/index.html'
    context_object_name = 'question_list'
    paginate_by = 2

    def get_queryset(self):
        """
        Sorts questions
        """
        return Question.objects.all().order_by('-date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'qa/detail.html'

    def get_queryset(self):
        """
        Sorts answers
        """
        return Question.objects.all().order_by('-date')


class QuestionCreate(CreateView):
    model = Question
    fields = '__all__'


class QuestionEdit(UpdateView):
    model = Question
    fields = ['subject', 'description', 'category']


class QuestionDelete(DeleteView):
    model = Question
    success_url = reverse_lazy('qa:index')
