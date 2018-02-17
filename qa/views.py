from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from .models import Question


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
