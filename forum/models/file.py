from forum.dao.sqlite3dao import DAO

def save_file(postid, filename, filetype):
    params = [ postid, filename, filetype ]
    sql = 'INSERT INTO files VALUES (?, ?, ?)'
    rowid = DAO().execute(sql, params)
    return rowid

def get_files_by_post(postid):
    sql = '''SELECT rowid, filename, filetype
            FROM files
            WHERE postid = ?'''    
    rs = DAO().get(sql, [ postid ])
    return rs if rs else False

def get_file(rowid):
    sql = 'SELECT filename, filetype FROM files WHERE rowid = ?'
    rs = DAO().get(sql, [ rowid ])
    return list.pop(rs) if rs else False

def get_allowed_filetypes():
    return [ 'jpg', 'gif', 'png', 'txt', 'pdf', 'doc', 'csv']
