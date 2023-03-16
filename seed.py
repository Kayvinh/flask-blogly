from models import User, db, Post
from app import app

db.drop_all()
db.create_all()

# Add Users
user1 = User(first_name='Kevin', last_name='Nguyen')
user2 = User(first_name='Joel', last_name='Burton')
user3 = User(first_name='Jane', last_name='Smith')

# Add new objects to session
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

# Add new posts
post1 = Post(title='A cool title', content= 'A cool article')
post2 = Post(title='A lame title', content= 'A lame article')

# Add posts to session
db.session.add(post1)
db.session.add(post2)

# commit
db.session.commit()