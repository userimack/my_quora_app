from django.db import models
from django.contrib.auth.models import User
#  from datetime import datetime
from django.utils import timezone
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns


class Category(models.Model):
    """
    Model representation for category
    """
    name = models.CharField(max_length=200, help_text="Enter the category")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Question(models.Model):
    """
    Model representation of an asked question
    """
    subject = models.CharField(max_length=200, help_text="Enter the subject of the question.")
    description = models.TextField(help_text="Enter the description of your question.")
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, help_text="Rate the question")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, help_text="Choose category")
    date = models.DateTimeField('date published', default=timezone.localtime)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        """
        Returns the url of the detailed page for the question
        """
        return reverse('qa:answer', args=[str(self.id)])


class Answer(models.Model):
    """
    Model representation of answer to the asked questions
    """
    question = models.ForeignKey(Question, help_text="Select question", on_delete=models.CASCADE)
    answer = models.TextField(help_text="Enter your answer")
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, help_text="Rate the answer")
    date = models.DateTimeField('date published', default=timezone.localtime)

    def __str__(self):
        return "{}...".format(self.answer[0:10])
