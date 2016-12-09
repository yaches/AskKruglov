from django import forms

from django.contrib.auth import authenticate
from django.contrib.auth.models import *
from django.core import validators

from .models import *

class CommaSeparatedCharField(forms.Field):
	def __init__(self, *args, **kwargs):
		super(CommaSeparatedCharField, self).__init__(*args, **kwargs)

	def to_python(self, value):
		if value in validators.EMPTY_VALUES:
			return []

		value = [item.strip() for item in value.split(',') if item.strip()]

		return value

	def clean(self, value):
		value = self.to_python(value)
		self.validate(value)
		self.run_validators(value)
		return value


class AnswerForm(forms.Form):
	text = forms.CharField(widget = forms.Textarea(attrs = {
		'class': 'form-control input-lg', 
		'placeholder': 'Enter your answer here',
		'rows': 5,
		}))

	def save(self, question_id, user_id = 228):
		data = self.cleaned_data
		answer = Answer(text = data['text'], question_id = question_id, author_id = user_id)
		answer.save()


class AskForm(forms.Form):
	title = forms.CharField(widget = forms.TextInput(attrs = {
		'class': 'form-control input-lg',
		'placeholder': 'Enter the title here'
		}))
	text = forms.CharField(widget = forms.Textarea(attrs = {
		'class': 'form-control input-lg', 
		'placeholder': 'Enter your question here',
		'rows': 20,
		}))
	tags = CommaSeparatedCharField(widget = forms.TextInput(attrs = {
		'class': 'form-control input-lg',
		'placeholder': 'Enter the tags separated by comma'
		}))

	def save(self, user_id):
		data = self.cleaned_data
		question = Question(title = data['title'], text = data['text'], author_id = user_id)
		question.save()
		tags = data['tags']
		for t in tags:
			tag = Tag.objects.tag_by_name(t)
			if tag is None:
				tag = Tag(name = t)
				tag.save()
			question.tags.add(tag)
		question.save()

		return question

class LoginForm(forms.Form):

	username = forms.CharField(widget = forms.TextInput(attrs = {
		'class': 'form-control input-lg',
		'placeholder': 'Enter your login here'
		}))
	password = forms.CharField(widget = forms.PasswordInput(attrs = {
		'class': 'form-control input-lg',
		'placeholder': 'Enter your password here'
		}))

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']

		self.user = authenticate(username = username, password = password)

		if self.user is None:
			raise forms.ValidationError('Wrong login or password!')



class SignUpForm(forms.Form):

	username = forms.CharField(widget = forms.TextInput(attrs = {
		'class': 'form-control input-lg',
		'placeholder': 'Enter your login here'
		}))
	email = forms.EmailField(widget = forms.EmailInput(attrs = {
		'class': 'form-control input-lg',
		'placeholder': 'Enter your e-mail here'
		}))
	password = forms.CharField(widget = forms.PasswordInput(attrs = {
		'class': 'form-control input-lg',
		'placeholder': 'Enter your password here'
		}))
	repeat_password = forms.CharField(widget = forms.PasswordInput(attrs = {
		'class': 'form-control input-lg',
		'placeholder': 'Repeat your password here'
		}))

	def clean_username(self):
		username = self.cleaned_data['username']
		if Profile.objects.exist_login(username):
			raise forms.ValidationError('Login is already exist!')
		return username

	def clean_repeat_password(self):
		data = self.cleaned_data
		if data['password'] != data['repeat_password']:
			raise forms.ValidationError('Different passwords!')
		return data['repeat_password']

	def clean_email(self):
		email = self.cleaned_data['email']
		if Profile.objects.exist_email(email):
			raise forms.ValidationError('Email is already exist!')
		return email

	def save(self):
		data = self.cleaned_data
		username = data['username']
		email = data['email']
		password = data['password']
		profile = Profile.objects.create_user(username = username, email = email, \
			password = password, nickname = nickname)


class SettingsForm(forms.Form):

	username = forms.CharField(widget = forms.TextInput(attrs = {
		'class': 'form-control input-lg',
		}))
	email = forms.EmailField(widget = forms.EmailInput(attrs = {
		'class': 'form-control input-lg',
		}))
	avatar = forms.ImageField()

	def clean_username(self):
		username = self.cleaned_data['username']
		if self.fields['username'].has_changed(initial = self.initial['username'], \
			data = username):
			if Profile.objects.exist_login(username):
				raise forms.ValidationError('Login is already exist!')
		return username

	def clean_email(self):
		email = self.cleaned_data['email']
		if self.fields['email'].has_changed(initial = self.initial['email'], \
			data = email):
			if Profile.objects.exist_email(email):
				raise forms.ValidationError('Email is already exist!')
		return email

	def save(self, user):
		data = self.cleaned_data
		user.username = data['username']
		user.email = data['email']
		user.avatar = data['avatar']
		user.save()


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags', ]

    def __init__(self, current_user, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['text'].widget.attrs.update({
            'class': 'form-control askme-textarea',
            'rows': 5,
        })
        self.fields['tags'].widget.attrs.update({
            'class': 'form-control'
        })
        self.current_user = current_user

    def save(self, commit=True):
        question = super(QuestionForm, self).save(commit=False)
        question.user = self.current_user
        if commit:
            question.save()
        return question.id