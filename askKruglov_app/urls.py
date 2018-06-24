# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views 

app_name = 'askKruglov_app'
urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^(?P<page_num>[0-9]+)/$', views.index, name = 'index'),
	url(r'^hot/$', views.hot, name = 'hot'),
	url(r'^hot/(?P<page_num>[0-9]+)/$', views.hot, name = 'hot'),
	url(r'^tag/(?P<tag_name>[\S]+)/$', views.tag, name = 'tag'),
	url(r'^tag/(?P<tag_name>[\S]+)/(?P<page_num>[0-9]+)/$', views.tag, name = 'tag'),
	url(r'^question/(?P<question_id>[0-9]+)/$', views.question, name = 'question'),
	url(r'^question/(?P<question_id>[0-9]+)/(?P<page_num>[0-9]+)/$', views.question, name = 'question'),
	url(r'^ask/$', views.ask, name = 'ask'),
	url(r'^login/$', views.login_view, name = 'login'),
	url(r'^logout/$', views.logout_view, name = 'logout'),
	url(r'^signup/$', views.signup, name = 'signup'),
	url(r'^settings/$', views.settings, name = 'settings'),
	url(r'^like_question/$', views.like_question, name = 'like_question'),
	url(r'^like_answer/$', views.like_answer, name = 'like_answer'),
	url(r'^correct/$', views.correct_answer, name = 'correct'),
	url(r'^search/$', views.search, name = 'search'),
]
