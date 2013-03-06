''' 
    Helper class to setup databases for initializing application,
    also used in testing modules to create/drop tables for testing
'''

from forum.dao.sqlite3dao import DAO
 
def create_threads_table():
    DAO().execute('''CREATE TABLE IF NOT EXISTS threads
                    (title text, create_date text) ''')

def create_posts_table():
    DAO().execute('''CREATE TABLE IF NOT EXISTS posts
                (threadid integer, title text, post_date text, 
                posted_by text, body text) 
               ''')

def create_users_table():
    DAO().execute('''CREATE TABLE IF NOT EXISTS users
                (username text, password text, role text, 
                unique(username) on conflict replace )
                ''')

def create_files_table():
    DAO().execute('''CREATE TABLE IF NOT EXISTS files
                (postid text, filename text, filetype text )
                ''')
    
def create_session_table():
    DAO().execute('''CREATE TABLE IF NOT EXISTS session
                (sessionid text, userid text, expiration text, unique(userid) on conflict replace )
                ''')
    
def drop_table(table):
    DAO().execute('DROP TABLE %s' % table)
    
if __name__ == '__main__':
    create_threads_table()
    create_posts_table()
    create_users_table()
    create_files_table()
    create_session_table()