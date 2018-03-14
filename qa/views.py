from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
#  from django.urls import reverse_lazy
#  from django.views.generic.edit import UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
#  from django.core.exceptions import PermissionDenied
#  from django.http import HttpResponse
import logging

from .models import Question, Answer  # , RateQuestion, RateAnswer
from .forms import QuestionForm, AnswerForm


logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    model = Question
    template_name = 'qa/index.html'
    context_object_name = 'question_list'
    paginate_by = 6


class DetailView(generic.DetailView):
    model = Question
    template_name = 'qa/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        return context


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
            question.created_at = timezone.now()
            question.updated_at = timezone.now()
            question.save()
            return redirect('qa:answers', pk=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'qa/question_form.html', {'form': form})


@login_required
def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk, contributor=request.user)
    logger.info(question)
    #  if question.contributor != request.user:
    #      raise PermissionDenied(u"You don't have permission to edit this.")
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.updated_at = timezone.now()
            question.save()
            return redirect('qa:answers', pk=question.pk)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'qa/question_form.html', {'form': form})


@login_required
def answer_edit(request, pk):
    answer = get_object_or_404(Answer, pk=pk, contributor=request.user)
    #  if answer.contributor != request.user:
    #      raise PermissionDenied(u"You don't have permission to edit this.")

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.updated_at = timezone.now()
            answer.save()
            return redirect('qa:answers', pk=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    return render(request, 'qa/answer_form.html', {'form': form})


@login_required
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk, contributor=request.user)
    #  if question.contributor != request.user:
    #      raise PermissionDenied(u"You don't have permission to delete this.")
    question.delete()
    return redirect('qa:index')


@login_required
def answer_delete(request, pk):
    answer = get_object_or_404(Answer, pk=pk, contributor=request.user)
    #  if answer.contributor != request.user:
    #      raise PermissionDenied(u"You don't have permission to delete this.")
    answer.delete()
    return redirect('qa:answers', pk=answer.question.id)


@login_required
def new_answer(request, pk):
    #  import pdb;pdb.set_trace()
    question = Question.objects.get(pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question_id = pk
            answer.contributor = request.user
            answer.created_at = timezone.now()
            answer.updated_at = timezone.now()
            answer.save()
            return redirect('qa:answers', pk=question.pk)
    else:
        form = AnswerForm()
    return render(request, 'qa/answer_form.html', {'form': form, 'question': question})


@login_required
def question_vote(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        # Checking which button was clicked
        upvote = True if "upvote" in request.POST else False

        if upvote:
            if not question.has_upvoted(request.user):
                question.upvote(request.user)
                if question.has_downvoted(request.user):
                    question.remove_downvote(request.user)
        else:
            if not question.has_downvoted(request.user):
                question.downvote(request.user)
                if question.has_upvoted(request.user):
                    question.remove_upvote(request.user)

    return redirect('qa:answers', pk=pk)


@login_required
def answer_vote(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if request.method == 'POST':
        # Checking which button was clicked
        upvote = True if "upvote" in request.POST else False

        if upvote:
            if not answer.has_upvoted(request.user):
                answer.upvote(request.user)
                if answer.has_downvoted(request.user):
                    answer.remove_downvote(request.user)
        else:
            if not answer.has_downvoted(request.user):
                answer.downvote(request.user)
                if answer.has_upvoted(request.user):
                    answer.remove_upvote(request.user)

    return redirect('qa:answers', pk=answer.question.id)
