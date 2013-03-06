import unittest

from forum.models.post import save_post, get_posts, get_posts_as_html
from forum.models.thread import save_thread
from forum.models.user import save_user
from setup_create_db import create_posts_table, create_threads_table, create_users_table, drop_table

class TestPost(unittest.TestCase):
    
    def setUp(self):
        create_users_table()
        create_posts_table()
        create_threads_table()
    
    def tearDown(self):
        drop_table('posts')
        drop_table('threads')
        drop_table('users')
    
    def test_save_get(self):
        save_user('admin', 'admin')
        save_thread('test')
        save_post(1, 'Test Post', 'admin', 'This is a test post')
        posts = get_posts(1)
        post = posts.pop()
        self.assertEqual(post['title'], u'Test Post')
    
if __name__ == '__main__':
    unittest.main()
        