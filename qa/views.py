from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
#  from django.urls import reverse_lazy
#  from django.views.generic.edit import UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import PermissionDenied
#  from django.http import HttpResponse

from .models import Question, Answer, RateQuestion, RateAnswer
from .forms import QuestionForm, AnswerForm


class IndexView(generic.ListView):
    model = Question
    template_name = 'qa/index.html'
    context_object_name = 'question_list'
    paginate_by = 6

    #  def get_context_data(self, **kwargs):
    #      context = super(IndexView, self).get_context_data(**kwargs)
    #      context['question_rating'] = RateQuestion.objects.filter(question=self.Question)
    #      return context


class DetailView(generic.DetailView):
    model = Question
    template_name = 'qa/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        #  print(context)
        upvoted_questions = RateQuestion.objects.filter(question=context["question"], rating=True)
        downvoted_question = RateQuestion.objects.filter(question=context["question"], rating=False)
        context['question_upvotes'] = upvoted_questions.count()
        context['question_upvoted_users'] = [rate_obj.user for rate_obj in upvoted_questions]
        context['question_downvotes'] = downvoted_question.count()
        context['question_downvoted_users'] = [rate_obj.user for rate_obj in downvoted_question]

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


@login_required
def question_vote(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.method == 'POST':
        rating = True if "upvote" in request.POST else False
        #  print("Rating = {}".format(rating))
        user = request.user
        rated_question = RateQuestion.objects.filter(question=question, user=user)

        #  total_votes = rated_question.count()
        #  print("rated_question: ", rated_question, total_votes)
        if len(rated_question) != 0:
            #  print("Total votes: ", total_votes)
            rated_question.delete()
            rating_obj = RateQuestion(user=user, question=question, rating=rating)
            rating_obj.save()
        else:
            rating_obj = RateQuestion(user=user, question=question, rating=rating)
            rating_obj.save()

    return redirect('qa:answers', pk=pk)


@login_required
def answer_vote(request, pk):
    answer = get_object_or_404(Answer, pk=pk)

    if request.method == 'POST':
        rating = True if "upvote" in request.POST else False
        user = request.user
        rated_answer = RateAnswer.objects.filter(answer=answer, user=user)

        if len(rated_answer) != 0:
            rated_answer.delete()
            rating_obj = RateAnswer(user=user, answer=answer, rating=rating)
            rating_obj.save()
        else:
            rating_obj = RateAnswer(user=user, answer=answer, rating=rating)
            rating_obj.save()

    return redirect('qa:answers', pk=pk)
