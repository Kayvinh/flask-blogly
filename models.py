from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://cdn.shopify.com/s/files/1/1061/1924/products/Emoji_Icon_-_Clown_emoji_grande.png?v=1571606089"

def connect_db(app):
    """ Connect to database. """

    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Models for Blogly."""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    first_name = db.Column(
        db.String(30),
        nullable=False
    )

    last_name = db.Column(
        db.String(30),
        nullable=False
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default=DEFAULT_IMAGE_URL
    )

    # direct navigation: User -> Post & back
    posts = db.relationship('Post', backref='user')

class Post(db.Model):
    """Posts for Blogly"""

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(
        db.String(30),
        nullable=False,
    )

    content = db.Column(
        db.Text,
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        default = datetime.now,
        nullable=False,
    )

    user_id= db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )