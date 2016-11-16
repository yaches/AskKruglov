from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse

from .models import *

def paginate(objects_list, page_num, in_page = 5):
	
	paginator = Paginator(objects_list, in_page)
	page = paginator.page(page_num)

	return page


def index(request, page_num = 1):

	questions = Question.objects.all()

	try:
		page = paginate(questions, page_num)
	except:
		return redirect('../')

	return render(request, 'askKruglov_app/index.html', {
			'page': page,
			'members': Profile.objects.best(),
			'tags': Tag.objects.populars(),
		})

def hot(request, page_num = 1):

	questions = Question.objects.hot()

	try:
		page = paginate(questions, page_num)
	except:
		return redirect('../')

	return render(request, 'askKruglov_app/hot.html', {
			'page': page,
			'members': Profile.objects.best(),
			'tags': Tag.objects.populars(),
		})

def tag(request, tag_name, page_num = 1):

	questions = Question.objects.tag(tag_name)

	try:
		page = paginate(questions, page_num)
	except:
		return redirect('../')

	return render(request, 'askKruglov_app/tag.html', {
			'page': page,
			'members': Profile.objects.best(),
			'tags': Tag.objects.populars(),
			'tag_name': tag_name,
		})

def question(request, question_id, page_num = 1):

	question = Question.objects.get(pk = question_id)
	answers = question.answer_set.all()

	try:
		page = paginate(answers, page_num, 2)
	except:
		return redirect('../')

	return render(request, 'askKruglov_app/question.html', {
			'question': question,
			'page': page,
			'id': question_id,
			'members': Profile.objects.best(),
			'tags': Tag.objects.populars(),
		})

def ask(request):
	return render(request, 'askKruglov_app/ask.html', {
			'members': Profile.objects.best(),
			'tags': Tag.objects.populars(),
		})

def login(request):
	return render(request, 'askKruglov_app/login.html', {
			'members': Profile.objects.best(),
			'tags': Tag.objects.populars(),
		})

def signup(request):
	return render(request, 'askKruglov_app/signup.html', {
			'members': Profile.objects.best(),
			'tags': Tag.objects.populars(),
		})

def settings(request):
	return render(request, 'askKruglov_app/settings.html', {
			'members': Profile.objects.best(),
			'tags': Tag.objects.populars(),
		})