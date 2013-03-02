import unittest

from setup_create_db import create_threads_table, drop_table
from forum.models.thread import save_thread, get_thread, get_threads

class TestThread(unittest.TestCase):
    
    def setUp(self):
        create_threads_table()
        
    def tearDown(self):
        drop_table('threads')
        
    def test_save_get(self):
        save_thread('Test Thread')
        thread = get_thread(1)
        self.assertEqual(thread['title'], u'Test Thread')
        
    def test_save_get_multiple_threads(self):
        save_thread('Thread 1')
        save_thread('Thread 2')
        save_thread('Thread 3')
        i = 0
        for thread in get_threads():
            i += 1
            self.assertEqual(thread['title'], u'Thread %s' % i)
        