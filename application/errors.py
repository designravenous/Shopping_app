from flask import render_template
from application import app, db

@app.errorhandler(404)
def not_found(error):
    message = 'File Not Found'
    return render_template('404.html', message=message), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    message = 'Internal Error'
    return render_template('500.html', message=message), 500
