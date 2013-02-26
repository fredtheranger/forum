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
        pass 
   
    '''if len(rs) == 1:
        row = rs[0]
        hashed_password = hash_password(password, row[2])
        print password, row[2], hashed_password
        if hashed_password == row[1]:
            u = User()
            u.rowid = row[0]
            u.username = username
            u.password = password
            u.realname = row[3]
            u.role = row[4],
            u.salt = row[2]
            return u
            '''
    
    return False

def get_user_by_username(username):
    rs = DAO().get('''SELECT rowid, password, realname, role 
                    FROM users
                    WHERE username = ?''', [ username ])
    if len(rs) == 1:
        x = list.pop(rs)
        u = User()
        u.rowid = x[0]
        u.username = username
        u.password = x[1]
        u.realname = x[2]
        u.role = x[3]
        return u
    return False

def get_user_by_id(rowid):
    return get_users(rowid)
     
def get_users(rowid = None):
    params = None
    sql = 'SELECT rowid, username, realname, role FROM users'
    if rowid:
        sql = sql + ' WHERE rowid = ?'
        params = [ rowid ]
        
    users = {}
    for row in DAO().get(sql, params):
        u = User()
        u.rowid = row[0]
        u.username = row[1]
        u.realname = row[2]
        u.role = row[3]
        
        users[row[0]] = u
        
    if rowid:
        return users.get(1)
    else:
        return users

class User:
    
    def __init__(self):
        self.rowid = None
        self.username = None
        self.password = None
        self.realname = None
        self.role = 'normal'
        
    def save(self):
        salt, enc_password = hash_password(self.password)
        enc_password_str = get_enc_password_str(salt, enc_password)
        params = [ self.username, enc_password_str, self.realname, self.role ]
        sql = 'UPDATE users SET username = ?, password = ?, realname = ?, role = ?'
        if self.rowid:
            sql = sql + ' WHERE rowid = ?'
            params.append(self.rowid)
        else:
            sql = 'INSERT INTO users VALUES (?, ?, ?, ?)'
            
        rowid = DAO().execute(sql, params)
        if not self.rowid:
            self.rowid = rowid
        
    def __str__(self):
        return self.username
        
        
        