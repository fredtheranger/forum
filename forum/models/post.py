from datetime import datetime

from forum.dao.sqlite3dao import DAO

class Post:
    
    def __init__(self):
        self.rowid = None
        self.title = None
        self.post_date = datetime.isoformat(datetime.now())
        self.posted_by = None
        self.body = None
        
    def save(self):
        params = [ self.title, self.post_date, self.posted_by, self.body ]
        if self.rowid:
            sql = 'UPDATE posts SET title = ?, post_date = ?, posted_by = ?, body = ? WHERE rowid = ?'
            params.append( self.rowid )
        else:
            sql = 'INSERT INTO posts VALUES (?, ?, ?, ?)'
        
        rowid = DAO().execute(sql, params)
        if not self.rowid:
            self.rowid = rowid
        
    @staticmethod
    def get(rowid = None):
        params = None
        sql = 'SELECT rowid, title, post_date, posted_by, body FROM posts'
        if rowid:
            sql = sql + ' WHERE rowid = ?'
            params = [ rowid ]
            
        posts = {}
        for row in DAO().get(sql, params):
            p = Post()
            p.rowid = row[0]
            p.title = row[1]
            p.post_date = row[2]
            p.posted_by = row[3]
            p.body = row[4]
            
            posts[row[0]] = p
        
        if rowid:
            return posts.get(1)
        else:    
            return posts
        
    def __str__(self):
        return self.title
        
 
