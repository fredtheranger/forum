import unittest

from forum.models.post import save_post, get_post, get_posts_as_html
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
        rowid = save_post('Test Post', 'mikec', 'This is a test post')
        post = get_post(rowid)
        self.assertEqual(post['title'], u'Test Post')
        
    def test_get_posts_as_html(self):
        save_post('Test Post', 'mikec', 'This is a test post')
        html = get_posts_as_html()
        regex = r'.*<h2>Test Post</h2>.*'
        self.assertRegexpMatches(html, regex)
        
        
if __name__ == '__main__':
    unittest.main()
        