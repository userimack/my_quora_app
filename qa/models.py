from django.db import models
from django.contrib.auth.models import User
#  from datetime import datetime
from django.utils import timezone
#  from django.urls import reverse  # Used to generate URLs by reversing the URL patterns


class Category(models.Model):
    """
    Model representation for category
    """
    name = models.CharField(max_length=200, help_text="Enter the category")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["-name"]


class Question(models.Model):
    """
    Model representation of an asked question
    """
    subject = models.CharField(max_length=200, help_text="Enter the subject of the question.")
    description = models.TextField(help_text="Enter the description of your question.")
    contributor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="question_contributor")
    total_upvotes = models.IntegerField(default=0, help_text="Total upvotes")
    upvoted_by_users = models.ManyToManyField(User, related_name="question_upvoted_by_users")
    total_downvotes = models.IntegerField(default=0, help_text="Total downvotes")
    downvoted_by_users = models.ManyToManyField(User, related_name="question_downvoted_by_users")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, help_text="Choose category")
    date = models.DateTimeField('date published', default=timezone.localtime)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ["-date"]


class Answer(models.Model):
    """
    Model representation of answer to the asked questions
    """
    question = models.ForeignKey(Question, help_text="Select question", on_delete=models.CASCADE)
    answer = models.TextField(help_text="Enter your answer")
    contributor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answer_contributor")
    total_upvotes = models.IntegerField(default=0, help_text="Total upvotes")
    upvoted_by_users = models.ManyToManyField(User, related_name="answer_upvoted_by_users")
    total_downvotes = models.IntegerField(default=0, help_text="Total downvotes")
    downvoted_by_users = models.ManyToManyField(User, related_name="answer_downvoted_by_users")
    date = models.DateTimeField('date published', default=timezone.localtime)

    def __str__(self):
        return self.answer[0:20]

    class Meta:
        ordering = ["-date"]
