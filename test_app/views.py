from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def index(request):

	content = '\
		<br><br> WSGI <br><br>\
		<form method="post">\
		<input type="text" name = "test">\
		<input type="submit" value="Send">\
		</form>'

	content += request.GET.urlencode()
	content += '<br>'
	content += request.POST.urlencode()

	response = HttpResponse(
		content,
		content_type = 'text/html',
		status = 200,
	)

	return response