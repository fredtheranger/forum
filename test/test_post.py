import unittest
from datetime import datetime

from forum.models.post import Post
from forum.dao.sqlite3dao import DAO

class TestPost(unittest.TestCase):
    
    def setUp(self):
        self.dao = DAO('forum.db')
        self.dao.execute('''CREATE TABLE posts
                      (title text, post_date text, 
                       posted_by text, body text) 
                       ''')
    
    def tearDown(self):
        self.dao.execute('DROP TABLE posts')
    
    def test_save_get(self):
        p = Post()
        p.title = 'Test Post'
        p.post_date = datetime.isoformat(datetime.now())
        p.posted_by = 'Mike'
        p.body = 'This is a test post'
                
        p.save()
        #print p.rowid
        
        post = Post.get(1)
        self.assertEqual(post.title, p.title)
        
if __name__ == '__main__':
    unittest.main()
        