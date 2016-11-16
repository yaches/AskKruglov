from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import Http404

from .models import *

def paginate(objects_list, page_num, in_page = 5):
	
	paginator = Paginator(objects_list, in_page)
	try:
		page = paginator.page(page_num)
	except:
		page = paginator.page(paginator.num_pages)

	return page


def index(request, page_num = 1):

	questions = Question.objects.all()

	page = paginate(questions, page_num)

	if int(page_num) != int(page.number):
		return redirect('askKruglov_app:index', page.number)

	return render(request, 'askKruglov_app/index.html', {
			'page': page,
			'members': Profile.objects.best(),
			'tags': Tag.objects.populars(),
		})

def hot(request, page_num = 1):

	questions = Question.objects.hot()

	page = paginate(questions, page_num)

	if int(page_num) != int(page.number):
		return redirect('askKruglov_app:hot', page.number)

	return render(request, 'askKruglov_app/hot.html', {
			'page': page,
			'members': Profile.objects.best(),
			'tags': Tag.objects.populars(),
		})

def tag(request, tag_name, page_num = 1):

	questions = Question.objects.tag(tag_name)
	if questions.count() == 0:
		raise Http404()

	page = paginate(questions, page_num)

	if int(page_num) != int(page.number):
		return redirect('askKruglov_app:tag', tag_name, page.number)

	return render(request, 'askKruglov_app/tag.html', {
			'page': page,
			'members': Profile.objects.best(),
			'tags': Tag.objects.populars(),
			'tag_name': tag_name,
		})

def question(request, question_id, page_num = 1):

	question = get_object_or_404(Question, pk = question_id)
	answers = question.answer_set.all()

	page = paginate(answers, page_num)

	if int(page_num) != int(page.number):
		return redirect('askKruglov_app:question', question_id, page.number)

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