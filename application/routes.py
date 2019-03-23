from application import app, bootstrap, db
from flask import render_template, url_for, flash, redirect, request
from application.forms import LoginForms, RegistrationForm, Add_Item_Form, Modify_item, RequestPasswordForm, Reset_PasswordForm
from application.models import User, ShoppingItems
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from application.email import send_email


@app.route('/')
@app.route('/index')
@login_required
def index():
    fetch_id = current_user.id
    form = Modify_item()
    user = current_user.username
    added_to_chart = []
    not_added = []
    posts = ShoppingItems.query.filter_by(user_id=current_user.id)
    for p in posts:
        if p.added_to_chart == True:
            added_to_chart.append(p)
        else:
            not_added.append(p)
    

    return render_template('index.html', added_to_chart=added_to_chart, not_added=not_added,user=user, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForms()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_hash(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if user.count_logged_in is None:
            user.count_logged_in = 1
        else:
            user.count_logged_in += 1
        user.last_logged_on = datetime.utcnow()
        db.session.commit()
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('New user: {}, is registered. Go ahead and login!'.format(form.username.data))
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/basket_status/<item_id>')
@login_required
def basket_status(item_id):
    item_to_change = ShoppingItems.query.filter_by(id=item_id).first()
    if item_to_change.added_to_chart == False:
        item_to_change.added_to_chart = True
    else:
        item_to_change.added_to_chart = False
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_new_item():
    form = Add_Item_Form()
    user = current_user.username
    current_user_id = User.query.filter_by(id=current_user.id).first()
    if form.validate_on_submit():
        added = form.item.data
        new_item = ShoppingItems(item=form.item.data, quantity=form.quantity.data, user_id=current_user.id)
        db.session.add(new_item)
        db.session.commit()
        flash('Item {} added'.format(added))
        return redirect(url_for('add_new_item'))
    return render_template('add_item.html', title="Add Item", form=form, user=user)

@app.route('/delete_added_items')
@login_required
def delete_added_items():
    users = User.query.filter_by(id=current_user.id).first()
    all_items = ShoppingItems.query.filter_by(user_id=users.id)
    for gross in all_items:
        if gross.added_to_chart == True:
            db.session.delete(gross)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_all_items')
@login_required
def delete_all_items():
    users = User.query.filter_by(id=current_user.id).first()
    all_items = ShoppingItems.query.filter_by(user_id=users.id)
    for item in all_items:
        db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/modify/<item_id>', methods=['GET', 'POST'])
def modify(item_id):
    form = Modify_item()
    nummer = int(item_id)
    db_item = ShoppingItems.query.get(nummer)
    db_item.item = form.item.data
    db_item.quantity = form.quantity.data
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_user')
@login_required
def delete_user():
    users_id = current_user.id
    user_name = current_user.username
    user_in_db = User.query.get(users_id)
    items_in_bag = ShoppingItems.query.filter_by(user_id=current_user.id)
    for posession in items_in_bag:
        db.session.delete(posession)
    db.session.delete(user_in_db)
    db.session.commit()
    flash("User Account for: {}, have been deleted".format(user_name))
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    user = current_user.username
    email = current_user.email
    last_logged_on = current_user.last_logged_on
    count_logged_in = current_user.count_logged_in
    return render_template('profile.html', user=user, title="Profile", email=email, last_logged_on=last_logged_on, count_logged_in=count_logged_in)

@app.route('/request_user_password', methods=['GET', 'POST'])
def request_user_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            sub = "[Remember2Buy] Reset Password"
            token = User.get_reset_password_token(user)
            html = render_template('email/reset_password.html', token=token,user=user)
            sender = app.config['ADMINS'][0]
            body = render_template('email/reset_password.txt', user=user, token=token)
            recipients = [user.email]
            send_email(sub, sender,recipients,body, html)
            flash('Message sent to {}'.format(user.email))
            return redirect('index')
        else:
            flash('Unable To Send Instructions, Email Not Found')
    return render_template('request_password.html', form=form)

@app.route('/reset_user_password/<token>', methods=['GET', 'POST'])
def reset_user_password(token):
    form = Reset_PasswordForm()
    token = token
    if form.validate_on_submit():
        return "success %s" % (token)
    return render_template('reset_password.html', form=form)