from django.core.management.base import BaseCommand, CommandError
from askKruglov_app.models import *
from django.db import transaction
import random

random.seed()

class Command(BaseCommand):

	# def add_arguments(self, parser):
	#        parser.add_argument('poll_id', nargs='+', type=int)
	def get_random_id(self, id_list):
		# id_list = obj_set.values_list('id', flat = True)
		index = random.randint(0, id_list.count() - 1)
		rand_id = id_list[index]
		return rand_id


	def fill_tags(self):
		n = 100
		with transaction.atomic():
			for i in range(1, n + 1):
				t = Tag(name = 'tag_' + str(i))
				try:
					t.save()
					self.stdout.write('Tag ' + str(i) + ' saved')
				except:
					self.stdout.write('Tag ' + str(i) + ' error')


	def fill_profiles(self):
		n = 100

		with transaction.atomic():
			for i in range (1, n + 1):
				username = 'user_' + str(i)
				password = '12345'
				try:
					user = Profile.objects.create_user(password = password, username = username)
					self.stdout.write('Profile ' + str(i) + ' saved')
				except:
					self.stdout.write('Profile ' + str(i) + ' error')


	def fill_questions(self):
		n = 1000

		author_id_list = Profile.objects.all().values_list('id', flat = True)
		tag_id_list = Tag.objects.all().values_list('id', flat = True)

		with transaction.atomic():
			for i in range(1, n + 1):
				num = str(i)
				title = 'question title ' + num
				text = ('questions text ' + num + ' ') * 10
				likes = random.randint(0, 100)

				author_id = self.get_random_id(author_id_list)
				# author = Profile.objects.get(pk = author_id)

				q = Question(title = title, text = text, likes = likes, author_id = author_id)
				q.save()
				for j in range(random.randint(1, 5)):
					tag_id = self.get_random_id(tag_id_list)
					# tag = Tag.objects.get(pk = tag_id)
					q.tags.add(tag_id)
				q.save()

				self.stdout.write('Question ' + str(i) + ' saved')


	def fill_answers(self):
		questions = Question.objects.all()
		questions_count = questions.count()
		author_id_list = Profile.objects.all().values_list('id', flat = True)

		with transaction.atomic():
			i = 0
			for q in questions:
				n = 100
				k = random.randint(0, n)
				i += 1
				for j in range(k):
					j += 1
					num = str(j)
					text = ('answer text ' + num + ' ') * 10
					likes = random.randint(0, 100)
					
					author_id = self.get_random_id(author_id_list)
					# author = Profile.objects.get(pk = author_id)

					a = Answer(text = text, likes = likes, author_id = author_id, question_id = q.id)
					a.save()
					self.stdout.write('Answer ' + str(j) + ' for question ' + str(i) + ' saved')

	def handle(self, *args, **options):
		self.fill_tags()
		self.fill_profiles()
		self.fill_questions()
		self.fill_answers()
