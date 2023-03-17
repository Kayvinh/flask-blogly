import os
from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db, Post, DEFAULT_IMAGE_URL


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
    return render_template('users/users.html', users=users)


@app.get('/users/new')
def new_user_form():
    """ Form for new user """

    return render_template('users/new_user_form.html')


@app.post('/users/new')
def new_user():
    """ Add new user and redirect to /users """

    fname_input = request.form['fname_input']
    lname_input = request.form['lname_input']
    image_input = request.form['image_input']

    if image_input is not None:
        image_input = DEFAULT_IMAGE_URL

    new_user = User(
        first_name=fname_input,
        last_name=lname_input,
        image_url=image_input
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.get('/users/<int:id>')
def user_detail(id):
    """ Display user detail """

    user = User.query.get_or_404(id)
    posts = user.posts

    return render_template(
        'users/detail.html',
        user=user,
        posts=posts
    )


@app.get('/users/<int:id>/edit')
def user_detail_edit(id):
    """ Display edit page for a user """

    user = User.query.get_or_404(id)

    return render_template('users/edit.html', user=user)


@app.post('/users/<int:id>/edit')
def user_detail_update(id):
    """Process the edit form, redirect user to /users"""

    user = User.query.get_or_404(id)
    user.first_name = request.form['fname_input']
    user.last_name = request.form['lname_input']
    user.image_url = request.form['image_input']

    # default doesnt get used on update, only insert
    db.session.commit()

    return redirect('/users')


@app.post('/users/<int:id>/delete')
def delete_user(id):
    """ Delete existing user """

    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

# Post Routes


@app.get("/users/<int:id>/posts/new")
def new_post_form(id):
    #TODO: change docsstring
    """Go to new post form"""

    user = User.query.get_or_404(id)

    return render_template('posts/new_post_form.html', user=user)


@app.post("/users/<int:id>/posts/new")
def user_post(id):
    #TODO: change docstring
    """ Display user post """

    user = User.query.get_or_404(id)

    title = request.form['title']
    content = request.form['content']

    post = Post(
        title=title,
        content=content,
        user_id=id
    )

    db.session.add(post)
    db.session.commit()

    return render_template(
        'posts/post.html',
        user=user,
        post=post
    )


@app.get("/posts/<int:id>")
def show_post_details(id):
    """Show post details"""

    # user = User.query.get_or_404(id)
    # post = Post.query.filter(Post.id==id).one()
    # user = post.user_id
    # user_info = User.query.filter_by(id=user).one()
    post = Post.query.get_or_404(id)

    return render_template("posts/post_detail.html", post=post)


@app.get("/posts/<int:id>/edit")
def edit_post(id):
    """Display edit post form """

    post = Post.query.get_or_404(id)

    return render_template('posts/edit_post.html', post=post)


@app.post("/posts/<int:id>/edit")
def post_update(id):
    """ Handle edit post """

    post = Post.query.get_or_404(id)
    #TODO: change name title_input
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.commit()

    return redirect(f'/posts/{id}')


@app.post("/posts/<int:id>/delete")
def delete_post(id):
    """ Handle delete post """

    post = Post.query.get_or_404(id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')
