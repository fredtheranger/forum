import unittest
from ConfigParser import NoOptionError

from forum.config.config import Config

class TestConfig(unittest.TestCase):
    
    def setUp(self):
        self.config = Config()
        
    def test_get_parameter(self):
        self.assertEqual(self.config.get('test.var'), 'value')
        
    def test_missing_parameter(self):
        with self.assertRaises(NoOptionError):
            self.config.get('test.missing')
        
if __name__ == '__main__':
    unittest.main()