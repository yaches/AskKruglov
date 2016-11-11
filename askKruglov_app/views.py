from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse

import random

random.seed()

questions = []
for i in range(1, 36000):
	questions.append( {'id': i, 'title': 'title ' + str(i) , 'body': ('  text-text-text-text-' + str(i)) * 10,
		'tags': ['tag' + str(i) + '_1', 'tag' + str(i) + '_2', 'tag' + str(i) + '_3'], 
		'author': 'author ' + str(i), 'likes': random.randint(-10, 10), 
		'answers': random.randint(0, 50)} )

members = []
for i in range(1, 6):
	members.append({'number': i, 'name': 'member ' + str(i)})

tags = []
for i in range(1, 17):
	tags.append({'name': 'tag' + str(i), 'weight': random.randint(1, 4)})

def paginate(objects_list, in_page, page_num):
	
	paginator = Paginator(objects_list, in_page)
	try:
		page = paginator.page(page_num)
	except:
		# page = paginator.page(1)
		raise Exception

	return page


def index(request, page_num = 1):

	try:
		page = paginate(questions, 5, page_num)
	except:
		return redirect('../')

	return render(request, 'askKruglov_app/index.html', {
			'page': page,
			'members': members,
			'tags': tags,
		})

def hot(request, page_num = 1):

	try:
		page = paginate(questions, 5, page_num)
	except:
		return redirect('../')

	return render(request, 'askKruglov_app/hot.html', {
			'page': page,
			'members': members,
			'tags': tags,
		})

def tag(request, tag_name, page_num = 1):

	try:
		page = paginate(questions, 5, page_num)
	except:
		return redirect('../')

	return render(request, 'askKruglov_app/tag.html', {
			'page': page,
			'members': members,
			'tags': tags,
			'tag_name': tag_name,
		})

def question(request, question_id, page_num = 1):

	try:
		page = paginate(questions, 5, page_num)
	except:
		return redirect('../')

	quest = questions[int(question_id) - 1]

	return render(request, 'askKruglov_app/question.html', {
			'question': quest,
			'page': page,
			'id': question_id,
			'members': members,
			'tags': tags,
		})

def ask(request):
	return render(request, 'askKruglov_app/ask.html', {
		'members': members,
		'tags': tags,
		})

def login(request):
	return render(request, 'askKruglov_app/login.html', {
		'members': members,
		'tags': tags,
		})

def signup(request):
	return render(request, 'askKruglov_app/signup.html', {
		'members': members,
		'tags': tags,
		})

def settings(request):
	return render(request, 'askKruglov_app/settings.html', {
		'members': members,
		'tags': tags,
		})