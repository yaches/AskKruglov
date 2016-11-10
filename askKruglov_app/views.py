from django.shortcuts import render
from django.core.paginator import Paginator
import random

random.seed()

# title = 'Question Title from views.py'
# body = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
# 		Donec ut mauris lacinia, semper tellus sit amet, ultricies augue. \
# 		Fusce et nulla vel justo imperdiet hendrerit eget ut ipsum. \
# 		Vestibulum fermentum rutrum erat, hendrerit blandit risus aliquet nec. \
# 		Nullam volutpat, risus ac laoreet accumsan, risus libero pharetra augue, \
# 		et iaculis risus mauris nec magna. Vivamus auctor est eu ante congue varius. \
# 		Nunc a est id tellus pellentesque lobortis id vitae leo. \
# 		Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. \
# 		Fusce erat ligula, sollicitudin ac semper vitae, malesuada in lorem.'
# tags = ['Mail.ru', 'Python', 'Django']
# author = 'Gogol'
# likes = 9
# answers = 8

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
		page = paginator.page(1)

	return page


def index(request, page_num = 1):

	page = paginate(questions, 5, page_num)

	return render(request, 'askKruglov_app/index.html', {
			'questions': page,
			'members': members,
			'tags': tags,
			# 'url_name': ['askKruglov_app:index', ''],
		})

def hot(request, page_num = 1):

	page = paginate(questions, 5, page_num)

	return render(request, 'askKruglov_app/hot.html', {
			'questions': page,
			'members': members,
			'tags': tags,
			# 'url_name': ['askKruglov_app:hot', ],
		})

def tag(request, tag_name, page_num = 1):

	page = paginate(questions, 5, page_num)

	return render(request, 'askKruglov_app/tag.html', {
			'questions': page,
			'members': members,
			'tags': tags,
			'tag_name': tag_name,
			# 'url_name': ['askKruglov_app:tag', str(tag_name)],
		})

def question(request, question_id, page_num = 1):

	page = paginate(questions, 5, page_num)
	try:
		question = questions[int(question_id) - 1]
	except:
		question = questions[0]

	return render(request, 'askKruglov_app/question.html', {
			'question': question,
			'answers': page,
			'id': question_id,
			'members': members,
			'tags': tags,
		})