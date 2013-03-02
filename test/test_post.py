import unittest

from forum.models.post import save_post, get_posts, get_posts_as_html
from setup_create_db import create_posts_table, drop_table

class TestPost(unittest.TestCase):
    
    def setUp(self):
        create_posts_table()
    
    def tearDown(self):
        drop_table('posts')
    
    def test_save_get(self):
        save_post(1, 'Test Post', 'mikec', 'This is a test post')
        posts = get_posts(1)
        post = posts.pop()
        self.assertEqual(post['title'], u'Test Post')
       
    def test_get_posts_as_html(self):
        save_post(1, 'Test Post', 'mikec', 'This is a test post')
        html = get_posts_as_html(1)
        regex = r'.*<h2>Test Post</h2>.*'
        self.assertRegexpMatches(html, regex)
    
if __name__ == '__main__':
    unittest.main()
        