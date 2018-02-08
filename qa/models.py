from django.db import models

# Create your models here.


class Question(models.Model):
    """
    Model representation of an asked question
    """
    subject = models.CharField(max_length=200, help_text="Enter the subject of the question.")
    description = models.TextField(help_text="Enter the description of your question.")

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

    def __str__(self):
        return "{}...".format(self.answer[0:10])
