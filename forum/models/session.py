from forum.dao.sqlite3dao import DAO
import hmac

def save_session(sessionid, userid, expiration):
    params = [ sessionid, userid, hmac.new(str(sessionid) + expiration).hexdigest(), expiration ]
    sql = 'INSERT INTO session VALUES (?, ?, ?, ?)'
    rowid = DAO().execute(sql, params)
    return rowid

def get_session(sessionid):
    sql = 'SELECT userid, token, expiration FROM session WHERE sessionid = ?'
    rs = DAO().get(sql, [ sessionid ] )
    return list.pop(rs) if rs else False