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

from .models import Question, Answer  # , RateQuestion, RateAnswer
from .forms import QuestionForm, AnswerForm


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
            question.date = timezone.now()
            question.save()
            return redirect('qa:answers', pk=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'qa/question_form.html', {'form': form})


@login_required
def question_edit(request, pk):
    # TODO: add contributor condition
    question = get_object_or_404(Question, pk=pk)
    print(question)

    if question.contributor != request.user:
        raise PermissionDenied(u"You don't have permission to edit this.")

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
            # TODO: updating question id
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


# TODO move these methods to helpers.py or utils.py
'''
upvote
check if user has upvoted previously.
if he didn't
'''
def remove_vote(object_name, upvote, user_obj):
    #  print("--remove--", object_name, upvote, user_obj)
    if upvote:
        object_name.total_upvotes -= 1
        object_name.upvoted_by_users.remove(user_obj)
    else:
        object_name.total_downvotes -= 1
        object_name.downvoted_by_users.remove(user_obj)
    object_name.save()


def add_vote(object_name, upvote, user_obj):
    #  print("--add--", object_name, upvote, user_obj)
    if upvote:
        object_name.total_upvotes += 1
        object_name.upvoted_by_users.add(user_obj)
    else:
        object_name.total_downvotes += 1
        object_name.downvoted_by_users.add(user_obj)
    object_name.save()


'''
case 1: upvote

case 2: downvote

case 3: previously upvoted and now you want to downvote.

case 4: previously downvoted and now you want to upvote.
'''

'''
question:
    upvote
    downvote


    upvote ->
     disabling upvote
     enable downvote

    downvote -> 
'''

# TODO: refactor this.
@login_required
def question_vote(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.method == 'POST':
        upvote = True if "upvote" in request.POST else False
        user = request.user

        reset_user_question_votes_to_zero(question, user)
        if upvote:
            # just remove both votes
            # reset to zero
            # upvote_question(question, user)
            question.upvote()
            # if user in question.downvoted_by_users.all():
                # remove_vote(question, False, user)

            # if user in question.upvoted_by_users.all():
                # remove_vote(question, True, user)
            # else:
                # add_vote(question, True, user)
        else:
            question.downvote()
            downvote_question(question, user)
            # if user in question.upvoted_by_users.all():
                # remove_vote(question, True, user)

            # if user in question.downvoted_by_users.all():
                # remove_vote(question, False, user)
            # else:
                # add_vote(question, False, user)

    return redirect('qa:answers', pk=pk)


@login_required
def answer_vote(request, pk):
    answer = get_object_or_404(Answer, pk=pk)

    if request.method == 'POST':
        vote = True if "upvote" in request.POST else False
        user = request.user

        if vote:
            if user in answer.downvoted_by_users.all():
                remove_vote(answer, False, user)

            if user in answer.upvoted_by_users.all():
                remove_vote(answer, True, user)
            else:
                add_vote(answer, True, user)
        else:
            if user in answer.upvoted_by_users.all():
                remove_vote(answer, True, user)
            if user in answer.downvoted_by_users.all():
                remove_vote(answer, False, user)
            else:
                add_vote(answer, False, user)

    return redirect('qa:answers', pk=answer.question.id)
