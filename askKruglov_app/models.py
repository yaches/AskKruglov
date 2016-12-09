# -*- coding^ utf-8 -*-

from django.db import models
from django.contrib.auth.models import *
from django.db.models import F, Count

# Create your models here.

class TagManager(models.Manager):
	def populars(self, num = 12):
		return self.annotate(q = Count('question')).order_by('-q')[:num]

	def tag_by_name(self, tag_name):
		tags = Tag.objects.filter(name = tag_name)
		if len(tags) > 0:
			return tags[0]
		else:
			return None

class ProfileManager(UserManager):
	def best(self, num = 5):
		# return self.annotate(n = Count('answer', distinct = True) + Count('question', distinct = True))\
		# .order_by('-n')[:num]
		# return self.annotate(n = Count('question')).order_by('-n')[:num]
		return self.order_by('-publications')[:num]

	def exist_login(self, username):
		user = Profile.objects.filter(username = username)
		if len(user) > 0:
			return True
		else:
			return False

	def exist_email(self, email):
		user = Profile.objects.filter(email = email)
		if (len(user) > 0):
			return True
		else:
			return False


class QuestionManager(models.Manager):
	def hot(self):
		return self.order_by('-likes')

	def tag(self, tag_name):
		return self.filter(tags__name = tag_name)

class Question(models.Model):
	title = models.CharField(max_length = 255)
	text = models.TextField()
	likes = models.PositiveIntegerField(default = 0)
	published_time = models.DateTimeField(auto_now_add = True)
	author = models.ForeignKey('Profile')
	tags = models.ManyToManyField('Tag')

	objects = QuestionManager()

	class Meta:
		ordering = ['-published_time']

	def answers_amount(self):
		return self.answer_set.count()

	def save(self, *args, **kwargs):
		if not self in self.author.question_set.all():
			self.author.publications += 1
			self.author.save()
		super(Question, self).save(*args, **kwargs)

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

	def save(self, *args, **kwargs):
		if not self in self.author.question_set.all():
			self.author.publications += 1
			self.author.save()
		super(Answer, self).save(*args, **kwargs)


class Tag(models.Model):
	name = models.CharField(max_length = 30, unique = True)
	# publications = models.IntegerField(default = 0)

	objects = TagManager()

	def __str__(self):
		return self.name


class Profile(User):
	publications = models.IntegerField(default = 0)
	# avatar = models.CharField(max_length = 255, blank = True)
	# avatar = models.ImageField(upload_to = '')

	avatar = models.ImageField(upload_to = 'avatars/', blank = False, max_length = 1000)
	# def get_filename(self):

	objects = ProfileManager()

	def avatar_path(self, default = False):
		# if default:
		# 	return './static/avatars/'
		# else:
		return './static/avatars/' + str(self.id) + '/'

	def recalculate(self):
		self.publications = self.question_set.count() + self.answer_set.count()
		self.save()
