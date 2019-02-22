from application import app, bootstrap, db
from flask import render_template, url_for, flash, redirect, request
from application.forms import LoginForms, RegistrationForm, Add_Item_Form, Modify_item
from application.models import User, ShoppingItems
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


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
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_hash(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
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

@app.route('/modify', methods=['GET', 'POST'])
def modify():
    shopping_items = ShoppingItems.query.filter_by(user_id=current_user.id)
    user = current_user.username
    return render_template('modify.html', title='Modify', shopping_items=shopping_items, user=user)

