from application import app, bootstrap
from flask import render_template, url_for, flash, redirect
from application.forms import LoginForms
from application.models import User
from flask_login import current_user, login_user, logout_user


@app.route('/')
@app.route('/index')
def index():
    user = 'Peter S Holgersson'
    posts = [{
        'item':'Kaffe',
        'user':'Sigge',
        'quantity':2
    },
    {
        'item':'sill',
        'user':'Roger',
        'quantity':3
    }
    ]
    return render_template('index.html', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForms()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_hash(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    login_user()
    return redirect(url_for('index'))