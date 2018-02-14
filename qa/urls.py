from django.conf.urls import url
from . import views

app_name = 'qa'  # To use the name in templates as {% url 'qa:index' %}
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^question/create/$', views.QuestionCreate.as_view(), name='question_create'),
    url(r'^question/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='answer'),
    url(r'^question/(?P<pk>[0-9]+)/edit/$', views.QuestionEdit.as_view(), name='question_edit'),
    url(r'^question/(?P<pk>[0-9]+)/delete/$', views.QuestionDelete.as_view(), name='question_delete'),
]
