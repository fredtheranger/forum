'''

http://lucumr.pocoo.org/2007/5/21/getting-started-with-wsgi/
'''
import re
from cgi import escape
from forum.models.post import Post

def _header(title = ''):
    html = '''
    <html>
    <head>
    <title>Forum :: %s</title>
    <link rel=stylesheet href="style.css" type="text/css" media=screen>
    </head>
    <body>
    <h1>Forum</h1>
    '''
    
    return html % title

def _footer():
    return '''
    <p>Footer</p>
    </body>
    </html>'''

def index(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    html = ''
    for key, p in Post.get().iteritems():
        post_html = '<h2><a href="/view/%s">%s</a></h2><h5>posted by %s on %s</h5><p>%s</p><br />' % ( key, p.title, p.posted_by, p.post_date, p.body )
        html += str(post_html)
    return [_header(), html, _footer()]

def view(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    args = environ['myapp.url_args']
    post_id = escape(args[0])
    return [_header(), post_id, _footer()]

def add(environ, start_response):
    # get the name from the url if it was specified there.
    args = environ['myapp.url_args']
    if args:
        subject = escape(args[0])
    else:
        subject = 'World'
    
    start_response('200 OK', [('Content-Type', 'text/html')])
    return ['''Hello %(subject)s
            Hello %(subject)s!

''' % {'subject': subject}]
    
def edit(environ, start_response):
    return [ 'edit post' ]

def not_found(environ, start_response):
    """Called if no URL matches."""
    start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    return ['Not Found']

# map urls to functions
urls = [
    (r'^$', index),
    (r'^view/(.+)$', view),
    (r'add/?$', add),
    (r'edit/(.+)$', edit)
]

def application(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex, callback in urls:
        match = re.search(regex, path)
        if match is not None:
            environ['myapp.url_args'] = match.groups()
            return callback(environ, start_response)
    return not_found(environ, start_response)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()