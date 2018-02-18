from django.conf.urls import url
from . import views

app_name = 'qa'  # To use the name in templates as {% url 'qa:index' %}
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^question/create/$', views.new_question, name='new_question'),
    url(r'^question/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='answers'),
    url(r'^question/(?P<pk>[0-9]+)/edit/$', views.QuestionEdit.as_view(), name='question_edit'),
    url(r'^question/(?P<pk>[0-9]+)/delete/$', views.QuestionDelete.as_view(), name='question_delete'),
    url(r'^answer/(?P<pk>[0-9]+)/new/$', views.new_answer, name='new_answer'),
    # url(r'^answer/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='answers'),
    url(r'^answer/(?P<pk>[0-9]+)/edit/$', views.AnswerEdit.as_view(), name='answer_edit'),
    url(r'^answer/(?P<pk>[0-9]+)/delete/$', views.AnswerDelete.as_view(), name='answer_delete'),
]


