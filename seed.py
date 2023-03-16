from models import User, db
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

# commit
db.session.commit()