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
    return render_template(
        'users.html',
        users=users
    )    #TODO: one liner


@app.get('/users/new')
def new_user():
    """ Form for new user """

    #TODO: change form.html to new_user_form.html
    return render_template('form.html')

@app.post('/users/new')
#TODO: use this func name up, flip func names
def new_user_form():
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
    #TODO: change fetch function
    user = User.query.filter(User.id == user_id).one()

    return render_template('detail.html',
                           user=user)

@app.get('/users/<int:user_id>/edit')
def user_detail_edit(user_id):
    """ Display edit page for a user """
        #TODO: change fetch function
    user = User.query.filter(User.id == user_id).one()

    return render_template('edit.html',
                           user=user)

@app.post('/users/<int:user_id>/edit')
#TODO: user_detail_update
def new_user_detail(user_id):
    """Process the edit form, redirect user to /users"""
        #TODO: change fetch function
    user = User.query.filter(User.id == user_id).one()
    user.first_name = request.form['fname_input']
    user.last_name = request.form['lname_input']
    user.image_url = request.form['image_input']

    # default doesnt get used on update, only insert

    db.session.commit()

    return redirect('/users')
#TODO: 2 line breaks inbetween classes and routes
@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """ Delete existing user """
        #TODO: change fetch function
    user = User.query.filter(User.id == user_id).one()

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
