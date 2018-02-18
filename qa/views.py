from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from .models import Question, Answer
from .forms import QuestionForm, AnswerForm


class IndexView(generic.ListView):
    model = Question
    template_name = 'qa/index.html'
    context_object_name = 'question_list'
    paginate_by = 6

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


#  class QuestionCreate(CreateView):
#      model = Question
#      fields = ['subject', 'description', 'category']


class QuestionEdit(UpdateView):
    model = Question
    fields = ['subject', 'description', 'category']


class QuestionDelete(DeleteView):
    model = Question
    success_url = reverse_lazy('qa:index')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created successfully.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def new_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.contributor = request.user
            question.date = timezone.now()
            question.save()
            return redirect('qa:answers', pk=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'qa/question_form.html', {'form': form})


def new_answer(request, pk):
    question = Question.objects.get(pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question_id = pk
            answer.contributor = request.user
            answer.date = timezone.now()
            answer.save()
            return redirect('qa:answers', pk=question.pk)
    else:
        form = AnswerForm()
    return render(request, 'qa/answer_form.html', {'form': form, 'question': question})


class AnswerEdit(UpdateView):
    model = Answer
    fields = ['subject', 'description', 'category']


class AnswerDelete(DeleteView):
    model = Answer
    success_url = reverse_lazy('qa:index')
