import sqlite3

class Singleton(object):
    _instance = None
 
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

class DAO(Singleton):

    def __init__(self, db = 'forum.db'):
        self._db = db
        self._connect()

    def _connect(self):
        self.c = sqlite3.connect(self._db)
    
    def _get_cursor(self):
        try:
            self.c.ping()
        except:
            self._connect()
        return self.c.cursor()
    
    def _commit(self):
        self.c.commit()

    def get(self, query, params = None):
        cur = self._get_cursor()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        return rows

    def execute(self, query, params = None):
        cur = self._get_cursor()
        if params:
            print params
            cur.execute(query, params)
        else:
            cur.execute(query)
        self._commit()
        rowid = cur.lastrowid
        cur.close()
        return rowid
        