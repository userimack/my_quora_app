#  from django import forms
#  from django.contrib.auth.models import User
#  from django.core.exceptions import ValidationError


#  class RegisterUserForm(forms.ModelForm):
#  password = forms.CharField(widget=forms.PasswordInput)
#  password2 = forms.CharField(widget=forms.PasswordInput)
#
#  class Meta:
#      model = User
#      fields = ['username', 'email']
#
#  # validate user
#  def clean_password(self):
#      cd = self.cleaned_data
#
#      if cd['password2'] != cd['password']:
#          raise ValidationError('Password don\'t match')
#
#          return cd['password']

from django import forms

from .models import Question, Answer, RateQuestion


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('subject', 'description', 'category',)


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('answer',)


class RateQuestionForm(forms.ModelForm):
    class Meta:
        model = RateQuestion
        fields = ('rating',)
