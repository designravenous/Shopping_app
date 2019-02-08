from application import app, bootstrap
from flask import render_template, url_for


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