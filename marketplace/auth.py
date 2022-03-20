from flask import ( 
    Blueprint, flash, render_template, request, url_for, redirect
) 
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from .forms import RegisterForm, LoginForm
from flask_login import login_user, login_required,logout_user, current_user
from . import db


#create a blueprint
bp = Blueprint('auth', __name__)

@bp.route("/register", methods=['GET', 'POST'])
def register():
	if (current_user.is_authenticated):
		return redirect(url_for('index'))
	form = RegisterForm()
	if form.validate_on_submit():
		username = form.username.data
		email = form.email.data
		email_exists = User.query.filter_by(email=email).first()
		if email_exists:
			flash(f'Email - {email} already exists, please login', 'Warning')
			return redirect(url_for('auth.login'))

		username_taken = User.query.filter_by(username=username).first()
		if username_taken:
			flash(f'Username - {username} already exists, please select a new username', 'Danger')
			return redirect(url_for('auth.register')) 

		pwd_hash = generate_password_hash(form.password.data)
		user = User(username=username, email = email, password=generate_password_hash(form.password.data))
		db.session.add(user)
		db.session.commit()
		flash(f'Your account has been create, please login!', 'success')
		return redirect(url_for('auth.login'))
	return render_template('register.html', title = 'Sign Up', form = form)

@bp.route("/login", methods=['GET', 'POST'])
def login():
	if (current_user.is_authenticated):
		return redirect(url_for('main.index'))
	form = LoginForm()
	if form.validate_on_submit():
	    user = User.query.filter_by(email = form.email.data).first()
	    if user and check_password_hash(user.password, form.password.data):
	    	login_user(user, True)
	    	return redirect(url_for('main.index'))
	    flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@bp.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('main.index'))


