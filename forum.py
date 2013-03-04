'''
    A (very) simple forum application.  The application allows all users to
    view threads and posts, but only authenticated users can create new threds
    and post new replies.  

    See included documentation for details on implementation design and security
    precautions: application-design.docx

    Helpful links:
        http://docs.python.org/2/library/cgi.html
        http://lucumr.pocoo.org/2007/5/21/getting-started-with-wsgi/
        http://www.python.org/dev/peps/pep-0333/#optional-platform-specific-file-handling
'''
import re
from cgi import escape
import cgi
import urllib
import os.path
from forum.models.post import get_posts_as_html, get_post_form, save_post
from forum.models.thread import get_threads_as_html, get_thread_form, save_thread
from forum.models.file import save_file, get_file, get_allowed_filetypes
from forum.config.config import Config

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
        if title:
            rowid = save_thread(escape(title))
            html = '<p>Thread saved. <a href="/thread/%s">Go to thread</a>.</p>' % rowid
        else:
            html = '''<p>Thread topic must not be blank, 
                <a href="javascript:" onclick="history.go(-1); return false">go back</a>.</p>'''
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
        
        if title and body:
            
            postid = save_post(threadid, escape(title), None, escape(body))
            
            # handle the file if needed
            fileitem = form['file']
            if fileitem.filename:
                fn = os.path.basename(fileitem.filename)
                ext = os.path.splitext(fn)[1][1:].lower()
                if any(ext in s for s in get_allowed_filetypes()):
                    save_path = os.path.join(Config().get('upload.dir'), fn)
                    open(save_path, 'wb').write(fileitem.file.read())
                    save_file(postid, fn, ext)
                    html = '<div><p>Post and upload saved. <a href="/thread/%s">Go to thread</a>.</p></div>' % threadid
                else:
                    html = '''<p>Filetype of [ %s ] is not allowed,
                            <a href="javascript:" onclick="history.go(-1); return false">go back</a>.</p>''' % ext
            else:
                html = '<div><p>Post saved. <a href="/thread/%s">Go to thread</a>.</p></div>' % threadid
                
        else:
            html = '''Post title and body must not be blank, 
                <a href="javascript:" onclick="history.go(-1); return false">go back</a>.</p>'''
    else:
        html = get_post_form()
        
    html = "%s\n%s\n%s" % ( _header(), html, _footer() )
        
    start_response('200 OK', [
        ('Content-Type', 'text/html; charset=utf-8'),
        ('Content-Length', str(len(html)))
    ])
    
    return [ html.encode('UTF-8') ]

def deliver_file(environ, start_response):
    
    args = environ['myapp.url_args']
    fileid = escape(args[0]) if args else None
    
    if fileid:
        f = get_file(fileid)
        filepath = os.path.join(Config().get('upload.dir'), f['filename'])
        if os.path.exists(filepath):
            fn = open(filepath, "rb")
            content_type = 'application/download'
            start_response( "200 OK", [
                            ('Content-Type', content_type),
                            ('Content-disposition', 'attachment; filename=%s' % str(os.path.basename(filepath)))
            ])
            return fn.read()
    
    start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    return ['Page Not Found']

def not_found(environ, start_response):
    """Called if no URL matches."""
    start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    return ['Page Not Found']

# map urls to functions
urls = [
    (r'^$', index),
    (r'^thread/([0-9]+)/?$', view_thread),
    (r'^thread/([0-9]+)/post/?$', add_post),
    (r'^thread/add/?$', add_thread),
    (r'^files/(.+)$', deliver_file)
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