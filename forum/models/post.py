from datetime import datetime

from forum.dao.sqlite3dao import DAO

def save_post(title, posted_by, body):
    params = [ title, datetime.isoformat(datetime.now()), posted_by, body ]
    sql = 'INSERT INTO posts VALUES (?, ?, ?, ?)'
    rowid = DAO().execute(sql, params)
    return rowid  

def get_post(rowid):
    return get_posts(rowid)      
    
def get_posts(rowid = None):
    params = None
    sql = 'SELECT rowid, title, post_date, posted_by, body FROM posts'
    
    if rowid:
        sql = sql + ' WHERE rowid = ?'
        params = [ rowid ]
    
    rs = DAO().get(sql, params) 
    if rs: 
        return list.pop(rs) if rowid else rs
    else:
        return False

def get_posts_as_html():
    html = '<div id="posts">\n'
    posts = get_posts()
    if not posts:
        html += '<p>There was an error.  Please contact the administrator.</p>\n'
    elif len(posts) > 0:
        for post in posts:
            html += '<div class="post">\n'
            html += '<h2>%s</h2>\n' % post['title']
            html += '<p class="dateline">Posted by %s on %s</p>\n' % ( post['posted_by'], post['post_date'] )
            html += '<p>%s</p>\n' % post['body']
            html += '</div>\n'
    else:
        html += '<p>No posts found.  Maybe you should <a href="/new">create one</a>.\n' 
    html += '</div>'
    
    return html