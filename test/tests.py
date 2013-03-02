import unittest
from test_config import TestConfig
from test_dao import TestDao
from test_files import TestFiles
from test_post import TestPost
from test_user import TestUser


def run():
    suite = unittest.TestSuite()
    suite.addTest(TestConfig)
    suite.addTest(TestDao)
    suite.addTest(TestFiles)
    suite.addTest(TestPost)
    suite.addTest(TestUser)
    suite.run()

if __name__ == '__main__':
    run()