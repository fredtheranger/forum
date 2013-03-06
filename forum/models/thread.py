'''
A thread is a collection of posts
'''

from datetime import datetime
from forum.dao.sqlite3dao import DAO

def save_thread(title):
    sql = 'INSERT INTO threads VALUES (?, ?)'
    params = [ title, datetime.isoformat(datetime.now()) ]
    rowid = DAO().execute(sql, params)
    return rowid

def get_thread(rowid):
    return get_threads(rowid)

def get_threads(rowid = None):
    params = None
    
    sql = '''SELECT threads.rowid, threads.title, 
                (SELECT COUNT(posts.rowid) FROM posts WHERE threadid = threads.rowid)  AS posts, 
                (SELECT MAX(posts.post_date) FROM posts WHERE threadid = threads.rowid) AS last_post 
            FROM threads;'''
    
    if rowid:
        sql += ' WHERE rowid = ?'
        params = [rowid]
        
    rs = DAO().get(sql, params)
    if rs:        
        return list.pop(rs) if rowid else rs
    else:
        return False
    
def get_threads_as_html():
    html = '<div id="threads">\n'
    html += '<p><a href="/thread/add">Create new topic</a></p>'
    threads = get_threads()
    if threads:
        html += '<table width="100%">\n'
        html += '<tr><th>Topic</th><th>Posts</th><th>Last post</th></tr>\n'
        for thread in threads:
            html += '<tr>\n'
            html += '<td><a href="/thread/%s">%s</a></td><td align="center">%s</td><td align="center">%s</td>\n' % (
                    thread['rowid'], thread['title'], thread['posts'], thread['last_post'])
            html += '</tr>\n'
            
        html += '</table>'
    else:
        html += '<p>No threads found.  Maybe you should <a href="/thread/add">create one</a></p>'
    html += '</div>\n'
    
    return html

def get_thread_form():
    html = '''
    <h2>New thread</h2>
    <div id="add-thread" class="form">
        <form id="form" name="form" method="post">
            <p>Add a new thread and start a discussion!</p>
            <label>Thread Topic: </label>
            <input type="text" name="title" id="title" />
            <input type="submit" name="submit" value="Create"/>
            <input type="button" name="cancel" value="Cancel" onclick="history.go(-1); return false"/> 
        </form>
    </div>
    '''
    return html




