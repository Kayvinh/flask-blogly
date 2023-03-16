import os
from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"

connect_db(app)

debug = DebugToolbarExtension(app)

@app.get('/')
def home():
    """ redirect to /users """
    return redirect('/users')


@app.get('/users')
def list_of_users():
    """ List users and has add user form """

    users = User.query.all()
    return render_template('users/users.html',users=users)


@app.get('/users/new')
def new_user_form():
    """ Form for new user """

    return render_template('users/new_user_form.html')


@app.post('/users/new')
def new_user():
    """ Add new user and redirect to /users """

    fname_input = request.form['fname_input']
    lname_input = request.form['lname_input']
    image_input = request.form['image_input']       # if empty string, passes in empty string

    # if empty is None
    new_user = User(
        first_name = fname_input,
        last_name = lname_input, 
        image_url = image_input
    )
    
    
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def user_detail(user_id):
    """ Display user detail """

    user = User.query.get_or_404(user_id)

    return render_template('users/detail.html',
                           user=user)


@app.get('/users/<int:user_id>/edit')
def user_detail_edit(user_id):
    """ Display edit page for a user """

    user = User.query.get_or_404(user_id)

    return render_template('users/edit.html',
                           user=user)


@app.post('/users/<int:user_id>/edit')
def user_detail_update(user_id):
    """Process the edit form, redirect user to /users"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['fname_input']
    user.last_name = request.form['lname_input']
    user.image_url = request.form['image_input']

    # default doesnt get used on update, only insert
    db.session.commit()

    return redirect('/users')



@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """ Delete existing user """

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
