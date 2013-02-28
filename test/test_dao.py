import unittest
from forum.dao.sqlite3dao import DAO

class TestDao(unittest.TestCase):
    
    def setUp(self):
        self.dao = DAO('forum.db')
        self.dao.execute('''CREATE TABLE posts
                            (title text, body text)
                            ''')
        
    def tearDown(self):
        self.dao.execute('DROP TABLE posts')
        
    def test_execute(self):
        pass
    
    def test_get(self):
        self.dao.execute('INSERT INTO posts VALUES ("post", "body")')
        r = self.dao.get('SELECT rowid, * FROM posts')
        self.assertEqual(r[0]['title'], 'post')
        self.assertEqual(r[0]['body'], 'body')
        
        
        
if __name__ == '__main__':
    unittest.main()