import sqlite3

DBNAME = '../forum.db'
 
conn = sqlite3.connect(DBNAME) 
 
cursor = conn.cursor()
 
# create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS posts
                (title text, post_date text, 
                posted_by text, body text) 
               ''')

cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (username text, password text, role text, 
                unique(username) on conflict replace )
                ''')

cursor.execute('''CREATE TABLE IF NOT EXISTS files
                (filename text, uploaded_by text, 
                file_type text, unique(filename) )
                ''')
