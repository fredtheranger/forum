import hashlib, uuid

from forum.dao.sqlite3dao import DAO

def hash_password(password, salt = uuid.uuid4().hex):
    ''' http://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python '''
    if password:
        hashed_password = hashlib.sha512(password + salt).hexdigest()
        return salt, hashed_password

def get_enc_password_str(salt, enc_password):
    return '%s::%s' % (salt, enc_password)  

def check_password(plain_password, enc_password_str):
    salt, enc_password = enc_password_str.split('::')
    salt, enc_password_new = hash_password(plain_password, salt)
    return True if enc_password_new == enc_password else False
     
def authenticate(username, password):
    user = get_user_by_username(username)
    
    if user:
        if check_password(password, user['password']):
            return user
    
    return False

def get_user_by_username(username):
    sql = '''SELECT rowid, username, password, role 
             FROM users
             WHERE username = ?'''
    rs = DAO().get(sql, [ username ])
    return list.pop(rs) if len(rs) == 1 else False

def get_user_by_id(rowid):
    return get_users(rowid)
     
def get_users(rowid = None):
    params = None
    sql = 'SELECT rowid, username, password, role FROM users'
    if rowid:
        sql = sql + ' WHERE rowid = ?'
        params = [ rowid ]
        
    rs = DAO().get(sql, params)    
    return list.pop(rs) if len(rs) == 1 else rs

def save_user(username, password, role='user'):
    salt, enc_password = hash_password(password)
    enc_password_str = get_enc_password_str(salt, enc_password)
    params = [ username, enc_password_str, role ]
    sql = 'INSERT INTO users VALUES (?, ?, ?)'
    rowid = DAO().execute(sql, params)
    return rowid

        
        
        