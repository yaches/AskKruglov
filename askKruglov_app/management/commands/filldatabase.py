from django.core.management.base import BaseCommand, CommandError
from askKruglov_app.models import *
from django.db import transaction

import random
import nltk
from nltk.corpus import words, names

random.seed()

nltk.download('words')
nltk.download('names')
words_list = words.words()
names_list = names.words()

class Command(BaseCommand):

	def add_arguments(self, parser):

		parser.add_argument('--tag',
			action = 'store_true',
			dest = 'tag',
			default = False)

		parser.add_argument('--profile',
			action = 'store_true',
			dest = 'profile',
			default = False)

		parser.add_argument('--question',
			action = 'store_true',
			dest = 'question',
			default = False)

		parser.add_argument('--answer',
			action = 'store_true',
			dest = 'answer',
			default = False)

	       
	def get_random_id(self, id_list):
		index = random.randint(0, id_list.count() - 1)
		rand_id = id_list[index]
		return rand_id

	def get_random_words(self, min_count, max_count):
		random_words = ''
		count = random.randint(min_count, max_count)
		for i in range(0, count):
			index = random.randint(0, len(words_list) - 1)
			random_words += words_list[index]
			if i != count - 1:
				random_words += ' '
		return random_words

	def get_random_name(self):
		index = random.randint(0, len(names_list) - 1)
		return names_list[index]

	def fill_tags(self):
		n = 100
		with transaction.atomic():
			for i in range(1, n + 1):
				word = self.get_random_words(1, 1)
				t = Tag(name = word)
				try:
					t.save()
					self.stdout.write('{}) Tag "{}" saved'.format(i, word))
				except:
					self.stdout.write('{}) Tag "{}" error'.format(i, word))


	def fill_profiles(self):
		n = 100
		with transaction.atomic():
			for i in range (1, n + 1):
				username = self.get_random_name()
				password = '12345'
				try:
					user = Profile.objects.create_user(password = password, username = username)
					self.stdout.write('{}) Profile "{}" saved'.format(i, username))
				except:
					self.stdout.write('{}) Profile "{}" error'.format(i, username))


	def fill_questions(self):
		n = 100

		author_id_list = Profile.objects.all().values_list('id', flat = True)
		tag_id_list = Tag.objects.all().values_list('id', flat = True)

		with transaction.atomic():
			for i in range(1, n + 1):
				title = self.get_random_words(3, 6)
				text = self.get_random_words(10, 20)
				# likes = random.randint(-100, 100)

				author_id = self.get_random_id(author_id_list)

				q = Question(title = title, text = text, likes = 0, author_id = author_id)
				q.save()
				for j in range(random.randint(1, 5)):
					tag_id = self.get_random_id(tag_id_list)
					q.tags.add(tag_id)
				q.save()

				self.stdout.write('{}) Question saved'.format(i))


	def fill_answers(self):
		questions = Question.objects.all()
		questions_count = questions.count()
		author_id_list = Profile.objects.all().values_list('id', flat = True)

		with transaction.atomic():
			i = 0
			for q in questions:
				n = 50
				k = random.randint(0, n)
				i += 1
				for j in range(k):
					j += 1
					num = str(j)
					text = self.get_random_words(10, 20)
					# likes = random.randint(0, 100)
					
					author_id = self.get_random_id(author_id_list)

					a = Answer(text = text, likes = 0, author_id = author_id, question_id = q.id)
					a.save()
					self.stdout.write('Answer {} for question {} saved'.format(j, i))


	def handle(self, *args, **options):
		if options['tag']:
			self.fill_tags()

		if options['profile']:
			self.fill_profiles()

		if options['question']:
			self.fill_questions()

		if options['answer']:
			self.fill_answers()