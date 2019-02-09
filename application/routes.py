from application import app, bootstrap
from flask import render_template, url_for, flash, redirect
from application.forms import LoginForms


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
    form = LoginForms()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)