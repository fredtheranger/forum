
from forum.models.user import save_user
import argparse

parser = argparse.ArgumentParser(description='Add a user to the forum.')
parser.add_argument('username', help='username')
parser.add_argument('password', help='password')

args = parser.parse_args()
username = args.username
password = args.password
if username and password:
    userid = save_user(username, password)
    print '%s saved to forum user table as user %s.' % ( username, userid )
else:
    print 'Could not save user to forum user table.'


    