# -*- coding^ utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models import F, Count

# Create your models here.

class TagManager(models.Manager):
	def populars(self, num = 12):
		return self.annotate(q = Count('question')).order_by('-q')[:num]

class ProfileManager(models.Manager):
	def best(self, num = 5):
		return self.annotate(n = Count('question') + Count('answer')).order_by('-n')[:num]

class Question(models.Model):
	title = models.CharField(max_length = 255)
	text = models.TextField()
	likes = models.PositiveIntegerField(default = 0)
	published_time = models.DateTimeField(auto_now_add = True)
	author = models.ForeignKey('Profile')
	tags = models.ManyToManyField('Tag')

	class Meta:
		ordering = ['-published_time']

	def answers_amount(self):
		return self.answer_set.count()

	def __str__(self):
		return self.title


class Answer(models.Model):
	text = models.TextField()
	likes = models.PositiveIntegerField(default = 0)
	published_time = models.DateTimeField(auto_now_add = True)
	author = models.ForeignKey('Profile')
	question = models.ForeignKey('Question')

	class Meta:
		ordering = ['published_time']


class Tag(models.Model):
	name = models.CharField(max_length = 30)

	objects = TagManager()

	def questions_amount(self):
		return self.question_set.count()

	def __str__(self):
		return self.name


class Profile(User):
	# avatar = models.CharField(max_length = 255, blank = True)
	# avatar = models.ImageField(upload_to = '')

	# def get_filename(self):

	objects = ProfileManager()

	def __str__(self):
		return self.username