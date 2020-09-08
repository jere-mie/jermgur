from flask import render_template, url_for, flash, redirect, request
from website import app, db
from website.forms import Register, Login, PostForm, ReplyForm
from website.models import User, Post, Reply
from flask_login import login_user, current_user, logout_user, login_required
import os

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    posts = Post.query.filter_by(public=True).all()
    # posts = Post.query.all()
    posts.reverse()
    return render_template('home.html', posts=posts)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/account', methods=['GET'])
@login_required
def account():
    posts = Post.query.filter_by(author=current_user).all()
    # posts = Post.query.all()
    posts.reverse()
    return render_template('account.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already authenticated','success')
        return redirect(url_for('home'))
    form = Register()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        if not os.path.exists(f"website/uploads/{form.username.data}"):
            os.mkdir(f"website/static/uploads/{form.username.data}")
        flash(f'Created account for {form.username.data}. You may now log in.', 'success')
        return redirect(url_for('login'))

    return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already authenticated','success')
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and form.password.data==user.password:
            login_user(user, remember=form.rememberMe.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Error Logging In', 'danger')
    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/newpost', methods=['GET', 'POST'])
@login_required
def newPost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user, public=form.public.data, image=form.image.data.filename)
        db.session.add(post)
        db.session.commit()
        form.image.data.save(f"website/static/uploads/{current_user.username}/"+form.image.data.filename)
        flash('You have successfully made a post!', 'success')
        return redirect(url_for("home"))
    return render_template("newPost.html", form=form, legend='Create a Post')

@app.route('/post/<post_id>/delete', methods=['GET','POST'])
@login_required
def deletePost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author!=current_user:
        flash('You cannot delete someone else\'s post!', 'danger')
        return redirect(url_for('home'))
    for reply in post.replies:
            db.session.delete(reply)
    db.session.delete(post)
    db.session.commit()
    os.remove(f'website/static/uploads/{current_user.username}/{post.image}')
    flash('Successfully deleted post!', 'success')
    return redirect(url_for('home'))

@app.route('/post/<post_id>/update', methods=['GET', 'POST'])
@login_required
def updatePost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author!=current_user:
        flash('You cannot update someone else\'s post!', 'danger')
        return redirect(url_for('home'))
    form = PostForm()
    
    if form.validate_on_submit():
        os.remove(f'website/static/uploads/{current_user.username}/{post.image}')
        post.title = form.title.data
        post.content = form.content.data
        post.image = form.image.data.filename
        post.public = form.public.data
        db.session.commit()
        form.image.data.save(f"website/static/uploads/{current_user.username}/"+form.image.data.filename)
        flash('You have successfully updated the post!', 'success')
        return redirect(url_for("home"))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.public.data = post.public
    return render_template("newPost.html", form=form, legend='Update Post')


@app.route('/post/<post_id>', methods=['GET', 'POST'])
def seePost(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/post/<post_id>/reply', methods=['GET', 'POST'])
def reply(post_id):
    post = Post.query.get_or_404(post_id)
    form = ReplyForm()
    if form.validate_on_submit():
        reply = Reply(title=form.title.data, content=form.content.data, writer=current_user, original=post)
        db.session.add(reply)
        db.session.commit()
        flash('You have successfully added a reply!', 'success')
        return render_template('post.html', post=post)
    return render_template("reply.html", form=form, legend='Reply to a Post')