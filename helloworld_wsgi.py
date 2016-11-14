from pprint import pformat
from cgi import parse_qs, escape

def application(environ, start_response):
    output = []

    output.append('<br><br> WSGI <br><br>')
    output.append('<form method="post">')
    output.append('<input type="text" name = "test">')
    output.append('<input type="submit" value="Send">')
    output.append('</form>')

    qs = parse_qs(environ['QUERY_STRING'])
    for k in qs:
    	output.append(k)
    	output.append(' = ')
    	output.append(qs[k][0])
    	output.append('<br>')
	
	output.append(pformat(environ['wsgi.input'].read()))
	output.append('<br>')

    start_response('200 OK', [('Content-Type', 'text/html')])
    return output
