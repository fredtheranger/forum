'''

http://lucumr.pocoo.org/2007/5/21/getting-started-with-wsgi/
'''
import re
from cgi import escape
import cgi
import urllib
from forum.models.post import get_posts_as_html, get_post_form, save_post
from forum.models.thread import get_threads_as_html, get_thread_form, save_thread

def _header(title = 'Home'):
    css = urllib.quote(open("style.css", "rb").read().encode("base64"))
    
    html = '''
    <html>
    <head>
    <title>Forum :: %s</title>
    <link rel=stylesheet href="data:text/css;base64,%s" type="text/css" media=screen>
    </head>
    <body>
    <div id="main">
    <div id="header">
    <h1><a href="/">A Simple Secure Forum</a></h1>
    </div>
    '''
    
    return html % ( title, css )

def _footer():
    return '''
    <div id="footer">
    <p>All posts reflect the opinion of the poster and not the forum owner.</p>
    </div>
    </div>
    </body>
    </html>'''

def index(environ, start_response):
    
    html = "%s\n%s\n%s" % ( _header(), get_threads_as_html(), _footer() )
        
    start_response('200 OK', [
        ('Content-Type', 'text/html; charset=utf-8'),
        ('Content-Length', str(len(html)))
    ])
    
    return [ html.encode('UTF-8') ]

def add_thread(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        title = form.getvalue("title")
        rowid = save_thread(title)
        html = '<div><p>Thread saved. <a href="/thread/%s">Go to thread</a>.</p></div>' % rowid
    else:
        html = get_thread_form()
        
    html = "%s\n%s\n%s" % ( _header(), html, _footer() )
        
    start_response('200 OK', [
        ('Content-Type', 'text/html; charset=utf-8'),
        ('Content-Length', str(len(html)))
    ])
    
    return [ html.encode('UTF-8') ]

def view_thread(environ, start_response):
    
    args = environ['myapp.url_args']
    threadid = escape(args[0]) if args else None
    
    html = "%s\n%s\n%s" % ( _header(), get_posts_as_html(threadid), _footer() )
        
    start_response('200 OK', [
        ('Content-Type', 'text/html; charset=utf-8'),
        ('Content-Length', str(len(html)))
    ])
    
    return [ html.encode('UTF-8') ]

def add_post(environ, start_response):
    
    args = environ['myapp.url_args']
    threadid = escape(args[0]) if args else None
   
    if environ['REQUEST_METHOD'] == 'POST':
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        title = form.getvalue("title")
        body = form.getvalue("body")
        save_post(threadid, title, None, body)
        html = '<div><p>Post saved. <a href="/thread/%s">Go to thread</a>.</p></div>' % threadid
    else:
        html = get_post_form()
        
    html = "%s\n%s\n%s" % ( _header(), html, _footer() )
        
    start_response('200 OK', [
        ('Content-Type', 'text/html; charset=utf-8'),
        ('Content-Length', str(len(html)))
    ])
    
    return [ html.encode('UTF-8') ]

def not_found(environ, start_response):
    """Called if no URL matches."""
    start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    return ['Not Found']

# map urls to functions
urls = [
    (r'^$', index),
    (r'^thread/([0-9]+)/?$', view_thread),
    (r'^thread/([0-9]+)/post/?$', add_post),
    (r'^thread/add/?$', add_thread)
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