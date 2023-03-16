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

# commit users
db.session.commit()

# Add new posts
post1 = Post(title='A cool title', content= 'A cool article', user_id=user1.id)
post2 = Post(title='A lame title', content= 'A lame article', user_id=user1.id)
post3 = Post(title='A very lame title', content= 'A lame article', user_id=user2.id)

# Add posts to session
db.session.add(post1)
db.session.add(post2)
db.session.add(post3)

# commit
db.session.commit()