from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    """
    Model representation of an asked question
    """
    subject = models.CharField(max_length=200, help_text="Enter the subject of the question.")
    description = models.TextField(help_text="Enter the description of your question.")
    contributer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.subject


class Answer(models.Model):
    """
    Model representation of answer to aksed question
    """
    question = models.ForeignKey(Question, help_text="Select question", on_delete=models.CASCADE)
    answer = models.TextField(help_text="Enter your answer")
    contributer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{}...".format(self.answer[0:10])


class QuestionRating(models.Model):
    """
    To store ratings for questions
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, help_text="Rate the question")
    contributer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.question.id} ({self.question.subject})'


class AnswerRating(models.Model):
    """
    To store ratings for questions
    """
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, help_text="Rate the answer")
    contributer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.answer.id} (Answer of {self.answer.question.subject})'
