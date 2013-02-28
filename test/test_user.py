import unittest

from forum.models.user import save_user, get_user_by_id, get_user_by_username, hash_password, check_password, get_enc_password_str, authenticate
from forum.dao.sqlite3dao import DAO

class TestUser(unittest.TestCase):
    
    def setUp(self):
        DAO('forum.db').execute('''CREATE TABLE users
                                (username text, password text, role text)
                                ''')
        save_user('mikec', 'secret')
        
    def tearDown(self):
        DAO('forum.db').execute('DROP TABLE users')
        
    def test_get_user_by_id(self):     
        user = get_user_by_id(1)
        self.assertEqual(user['username'], u'mikec')
        self.assertEqual(user['role'], u'user')
        
    def test_get_user_by_username(self):
        user = get_user_by_username('mikec')
        self.assertEqual(user['username'], u'mikec')
        
    def test_check_password(self):
        password = 'secret'
        salt, enc_pw = hash_password(password)
        enc_pw_str = get_enc_password_str(salt, enc_pw)
        self.assertTrue(check_password(password, enc_pw_str))
        
    def test_authenticate(self):
        user = authenticate('mikec','secret')
        self.assertTrue(user)
        self.assertEqual(user['username'], u'mikec')  
        
if __name__ == '__main__':
    unittest.main()
        