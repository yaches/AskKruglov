from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import redirect

# Create your views here.

# @csrf_exempt
# def helloworld(request):

# 	content = '\
# 		<br><br> WSGI <br><br>\
# 		<form method="post">\
# 		<input type="text" name = "test">\
# 		<input type="submit" value="Send">\
# 		</form>'

# 	content += request.GET.urlencode()
# 	content += '<br>'
# 	content += request.POST.urlencode()

# 	response = HttpResponse(
# 		content,
# 		content_type = 'text/html',
# 		status = 200,
# 	)

# 	return response

questions = []
for i in range(100):
	questions.append({'author': 'Author ' + str(i), 'title': 'title ' + str(i), 
		'body': 'body ' + str(i)})

def paginate(objects_list, in_page, page_num):
    paginator = Paginator(objects_list, in_page)
    page = paginator.page(page_num)
    return page

def index(request, page_num = 0):
    page = paginate(questions, 5, page_num)
    return render(request, 'test_app/index.html', {
		'questions': page,
	})

def tag(request, tag_name, page_num = 0):
    if page_num == 0:
        return redirect(tag_name + '/1')
    page = paginate(questions, 5, page_num)
    return render(request, 'test_app/tag.html', {
		'questions': page,
        'tag_name': tag_name,
	})