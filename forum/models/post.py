from datetime import datetime
import urllib

from forum.dao.sqlite3dao import DAO
from forum.models.file import get_files_by_post, get_allowed_filetypes

def save_post(threadid, title, posted_by, body):
    params = [ threadid, title, datetime.isoformat(datetime.now()), posted_by, body ]
    sql = 'INSERT INTO posts VALUES (?, ?, ?, ?, ?)'
    rowid = DAO().execute(sql, params)
    return rowid  

def get_posts(threadid):
    sql = '''SELECT p.rowid AS rowid, p.title AS title, 
                post_date, posted_by, body, t.title AS topic
            FROM posts p INNER JOIN threads t ON p.threadid = t.rowid
            WHERE p.threadid = ?'''
    params = [ threadid ]
    
    rs = DAO().get(sql, params) 
    
    return rs if rs else False

def get_posts_as_html(threadid):
    html = '<div id="posts">\n'
    posts = get_posts(threadid)
    #if not posts:
    #    html += '<p>There was an error.  Please contact the administrator.</p>\n'
    if posts:
        html += '<h2>%s</h2>\n' % posts[0]['topic']
        html += '<p><a href="/">Home</a> | <a href="/thread/%s/post">Reply</a></p>\n' % threadid
        for post in posts:
            html += '<div class="post">\n'
            html += '<h3>%s</h3>\n' % post['title']
            html += '<p class="dateline">Posted by %s on %s</p>\n' % ( post['posted_by'], post['post_date'] )
            html += '<p>%s</p>\n' % post['body']
                
            # Check for downloads
            files = get_files_by_post(post['rowid'])
            if files:
                html += '<p>\n'
                for f in files:
                    html += '<a href="/files/%s">%s</a>\n' % ( f['rowid'], f['filename'] )   
                html += '</p>\n'
                
            html += '</div>\n'
    else:
        html += '<p>No posts found.  Maybe you should <a href="/thread/%s/post">create one</a>.\n'  % threadid
    html += '</div>'
    
    return html

def get_post_form():
    icon_question_mark = urllib.quote(open("images/icon_question_mark.gif", "rb").read().encode("base64"))
    
    html = """
    <div id="add-post" class="form">
        <form id="form" name="form" method="post" enctype="multipart/form-data">
        <h2>New post</h2>
        <p>Add your $0.02 to the forum. Please don't try any funny business!</p>
        
        <label>Subject</label>
        <input type="text" name="title" id="title" size="50"/>
        <br />
        <textarea name="body" id="body" rows="10" cols="60"></textarea>
        <br />
        Add file (optional): 
        <a href="javascript:;" onclick="alert('Allowed filetypes: %s')">
            <img src="data:image/gif;base64,%s" height="20px" width="20px" />
        </a>
        <input type="file" name="file">
        <br />
        <input type="submit" name="submit" value="Add" />
        <input type="button" name="cancel" value="Cancel" onclick="history.go(-1); return false"/> 
        </form>
    </div>
    """ % ( ', '.join(get_allowed_filetypes()), icon_question_mark )
    
    return html