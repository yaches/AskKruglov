# -*- coding^ utf-8 -*-

from django.db import models

# Create your models here.

class ArticleManager(models.Manager):

	def published(self):
		return self.filter(is_published = True)

class Article(models.Model):
	title = models.CharField(max_length = 255, verbose_name = u'Title')
	text = models.TextField(verbose_name = u'Text')
	is_published = models.BooleanField(default = False, verbose_name = u'Published')
	author = models.ForeignKey('Author')

	objects = ArticleManager()

	class Meta:
		verbose_name = u'Article'
		verbose_name_plural = u'Articles'

	def __unicode__(self):
		return self.title

class Author(models.Model):
	name = models.CharField(max_length = 255, verbose_name = u'Name')
	birthday = models.DateField(null = False, blank = False, verbose_name = u'Birthday')

	class Meta:
		verbose_name = u'Author'
		verbose_name_plural = u'Authors'

	def __unicode__(self):
		return self.name
		# return u"{}{}".format(self.name, self.birthday)

class BlaBla(models.Model):
	bla = models.CharField(max_length = 155)