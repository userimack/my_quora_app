from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
#  from django.urls import reverse_lazy
#  from django.views.generic.edit import UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import PermissionDenied

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


#  class QuestionEdit(UpdateView):
#      model = Question
#      fields = ['subject', 'description', 'category']
#
#
#  class QuestionDelete(DeleteView):
#      model = Question
#      success_url = reverse_lazy('qa:index')


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


@login_required
def question_new(request):
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


@login_required
def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)
    print(question)
    if question.contributor != request.user:
        raise PermissionDenied(u"You don't have permission to edit this.")
    #  if request.user
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.contributor = request.user
            question.date = timezone.now()
            question.save()
            return redirect('qa:answers', pk=question.pk)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'qa/question_form.html', {'form': form})


@login_required
def answer_edit(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if answer.contributor != request.user:
        raise PermissionDenied(u"You don't have permission to edit this.")

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question_id = pk
            answer.contributor = request.user
            answer.date = timezone.now()
            answer.save()
            return redirect('qa:answers', pk=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    return render(request, 'qa/answer_form.html', {'form': form})


@login_required
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if question.contributor != request.user:
        raise PermissionDenied(u"You don't have permission to delete this.")
    question.delete()
    return redirect('qa:index')


@login_required
def answer_delete(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if answer.contributor != request.user:
        raise PermissionDenied(u"You don't have permission to delete this.")
    answer.delete()
    return redirect('qa:answers', pk=answer.question.id)


@login_required
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
