#from post import Post

#post = Post('Another test post', '2013-02-24', 'Mike', 'This is a test post...')
#post.save()

#print Post.get()
 
from forum.dao.sqlite3Dao import DAO

dao = DAO()
#print dao.get('select rowid, * from posts where rowid = ?', '2')

dao.execute('insert into posts values (?, ?, ?, ?)', ('t', 'p_d', 'p', 'b') )

print dao.get('select rowid, * from posts')