# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import Http404
from django.http import JsonResponse

from django.contrib.auth import *

from .models import *
from .forms import *
from .documents import *

from elasticsearch_dsl.query import MultiMatch, Match

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

	user = request.user

	question = get_object_or_404(Question, pk = question_id)
	answers = question.answer_set.all()	
	page = paginate(answers, page_num)

	if request.method == 'POST':
		form = AnswerForm(request.POST)
		if form.is_valid():
			form.save(question_id, user.id)
			return redirect('askKruglov_app:question', question_id, page.paginator.num_pages + 1)
	else:
		form = AnswerForm()

	if int(page_num) != int(page.number):
		return redirect('askKruglov_app:question', question_id, page.number)

	return render(request, 'askKruglov_app/question.html', {
			'form': form,
			'question': question,
			'page': page,
			'id': question_id,
			'members': Profile.objects.best(),
			'tags': Tag.objects.populars(),
		})

def ask(request):

	user = request.user
	if not user.is_authenticated():
		next_url = reverse('askKruglov_app:ask')
		login_url = reverse('askKruglov_app:login')
		return redirect(login_url + '?next=' + next_url)

	if request.method == 'POST':
		form = AskForm(request.POST)
		if form.is_valid():
			question = form.save(user.id)
			return redirect('askKruglov_app:question', question.id)
	else:
		form = AskForm()

	return render(request, 'askKruglov_app/ask.html', {
			'form': form,
			'members': Profile.objects.best(),
			'tags': Tag.objects.populars(),
		})

def login_view(request):

	user = request.user
	if user.is_authenticated():
		return redirect('askKruglov_app:index')

	next_page = request.GET.get('next')
	if next_page is None:
		next_page = 'askKruglov_app:index'

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			login(request, form.user)
			return redirect(next_page)
	else:
		form = LoginForm()

	return render(request, 'askKruglov_app/login.html', {
			'form': form,
			'members': Profile.objects.best(),
			'tags': Tag.objects.populars(),
		})

def logout_view(request):
	logout(request)
	next_page = request.GET.get('next')

	if next_page:
		return redirect(next_page)
	else:
		return redirect('askKruglov_app:index')

def signup(request):

	user = request.user

	if user.is_authenticated():
		return redirect('askKruglov_app:login')

	if request.method == 'POST':
		form = SignUpForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			user = authenticate(
				username = form.cleaned_data['username'],
				password = form.cleaned_data['password'] )
			auth.login(request, user)
			return redirect('askKruglov_app:login')
	else:
		form = SignUpForm()

	return render(request, 'askKruglov_app/signup.html', {
			'form': form,
			'members': Profile.objects.best(),
			'tags': Tag.objects.populars(),
		})

def settings(request):

	user = request.user

	if not user.is_authenticated():
		return redirect('askKruglov_app:index')

	data = {'username': user.username, 'email': user.email}
	if request.method == 'POST':
		form = SettingsForm(request.POST, request.FILES, initial = data)
		if form.is_valid():
			form.save(user.profile)
	else:
		form = SettingsForm(initial = data)
		
	return render(request, 'askKruglov_app/settings.html', {
			'form': form,
			'members': Profile.objects.best(),
			'tags': Tag.objects.populars(),
		})

def like_question(request):
	
	user = request.user

	if not user.is_authenticated():
		return JsonResponse({'status': 'error'})
	
	if request.method == "POST":
		question_id = request.POST.get('id', 0)
		like_type = bool(int(request.POST.get('type', 1)))

		try:
			question = Question.objects.get(pk = question_id)
		except:
			return JsonResponse({'status': 'error'})

		try:
			like = QuestionLike.objects.get(profile = user.profile, question = question)
			if like.like_type == like_type:
				like.delete()
			else:
				like.like_type = like_type
				like.save()
		except:
			like = QuestionLike(profile = user.profile, question = question, like_type = like_type)
			like.save()

		question.recalculate()
		return JsonResponse({'status': 'ok', 'likes': question.likes})

	return redirect('askKruglov_app:index')


def like_answer(request):

	user = request.user

	if not user.is_authenticated():
		return JsonResponse({'status': 'error'})
	
	if request.method == "POST":
		answer_id = request.POST.get('id', 0)
		like_type = bool(int(request.POST.get('type', 1)))

		try:
			answer = Answer.objects.get(pk = answer_id)
		except:
			return JsonResponse({'status': 'error'})

		try:
			like = AnswerLike.objects.get(profile = user.profile, answer = answer)
			if like.like_type == like_type:
				like.delete()
			else:
				like.like_type = like_type
				like.save()
		except:
			like = AnswerLike(profile = user.profile, answer = answer, like_type = like_type)
			like.save()

		answer.recalculate()
		return JsonResponse({'status': 'ok', 'likes': answer.likes})

	return redirect('askKruglov_app:index')


def correct_answer(request):

	user = request.user

	if request.method == "POST":
		answer_id = request.POST.get('id', 0)

		try:
			answer = Answer.objects.get(pk = answer_id)
		except:
			return JsonResponse({'status': 'error'})

		if user.profile == answer.question.author:
			answer.correct = not answer.correct
			answer.save()
			return JsonResponse({'status': 'ok', 'correct': answer.correct})
		else:
			return JsonResponse({'status': 'error'})

	return redirect('askKruglov_app:index')

def search(request, page_num = 1):
	query = request.GET.get('query')

	match = MultiMatch(query = query, fields=['title', 'text'])

	questions = QuestionDocument.search().query(match).to_queryset()

	page = paginate(questions, page_num)

	if int(page_num) != int(page.number):
		return redirect('askKruglov_app:search', page.number)

	return render(request, 'askKruglov_app/index.html', {
			'page': page,
			'members': Profile.objects.best(),
			'tags': Tag.objects.populars(),
			'search_value': query,
		})