from datetime import datetime

from forum.dao.sqlite3dao import DAO

def save_post(threadid, title, posted_by, body):
    params = [ threadid, title, datetime.isoformat(datetime.now()), posted_by, body ]
    sql = 'INSERT INTO posts VALUES (?, ?, ?, ?, ?)'
    rowid = DAO().execute(sql, params)
    return rowid  

def get_posts(threadid):
    sql = '''SELECT rowid, title, post_date, posted_by, body 
            FROM posts
            WHERE threadid = ?'''
    params = [ threadid ]
    
    rs = DAO().get(sql, params) 
    
    return rs if rs else False

def get_posts_as_html(threadid):
    html = '<div id="posts">\n'
    posts = get_posts(threadid)
    #if not posts:
    #    html += '<p>There was an error.  Please contact the administrator.</p>\n'
    if posts:
        for post in posts:
            html += '<div class="post">\n'
            html += '<h2>%s</h2>\n' % post['title']
            html += '<p class="dateline">Posted by %s on %s</p>\n' % ( post['posted_by'], post['post_date'] )
            html += '<p>%s</p>\n' % post['body']
            html += '</div>\n'
    else:
        html += '<p>No posts found.  Maybe you should <a href="/thread/%s/post">create one</a>.\n'  % threadid
    html += '</div>'
    
    return html

def get_post_form():
    html = """
    <div id="add-post" class="form">
        <form id="form" name="form" method="post">
        <h2>New post</h2>
        <p>Add your $0.02 to the forum. Please don't try any funny business!</p>
        
        <label>Subject</label>
        <input type="text" name="title" id="title" size="50"/>
        <br />
        <textarea name="body" id="body" rows="10" cols="60"></textarea>
        <br />
        <input type="submit" name="submit" value="Add" />
        </form>
    </div>
    """
    return html