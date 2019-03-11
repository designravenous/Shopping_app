import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # ..Config to DB
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-never-find-out'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = '*******@gmail.com'
    MAIL_PASSWORD = '**********'
    ADMINS = ['*********@gmail.com']

