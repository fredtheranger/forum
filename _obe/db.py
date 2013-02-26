import sqlite3

class DB:
    DBNAME = 'forum.db'
    
    def __init__(self):
        self.conn = sqlite3.connect(self.DBNAME)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
     
    #@staticmethod   
    #def insert_post(post):     
    #    db = DB()
    #    db.c.execute('INSERT INTO posts VALUES ("%s", "%s", "%s", "%s")' % 
    #                   ( post.title, post.post_date, post.posted_by, post.body))
    #    db.conn.commit()
    
    #@staticmethod   
    #def get_posts(rowid = None):
        #sql = "SELECT * FROM albums WHERE artist=?"
        #self.cur.execute(sql, [("Red")])
        #self.cur.execute(sql)
        #print self.cur.fetchall()  # or use fetchone()
        #db = DB()
        #posts = {}
        #sql = 'SELECT rowid, * FROM posts'
        #for row in db.c.execute(sql):
        #    posts[row['rowid']] = row
        #db.c.execute(sql)
        #return db.c.fetchall()
        
    @staticmethod
    def insert(sql, params):
        db = DB()
        db.c.execute(sql, params)
        db.conn.commit()
        return True
    
    @staticmethod
    def query(sql):
        db = DB()
        db.c.execute(sql)
        return db.c.fetchall()


    