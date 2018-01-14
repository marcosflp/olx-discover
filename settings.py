import os
from logging.config import dictConfig
from decouple import config

BASEDIR = os.path.abspath(os.path.dirname(__file__))


# Security

DEBUG = config('DEBUG', default=True, cast=bool)
ADMINS = frozenset(['marcos.fel93@gmail.com'])

SECRET_KEY = config('SECRET_KEY', default='4cn68iga94@**2x9vb1f*-104pe%%*-u-%%#%%1wh!r(+mjiza@y$', cast=str)
CSRF_ENABLED = config('CSRF_ENABLED', default=True, cast=bool)
CSRF_SESSION_KEY = config('CSRF_SESSION_KEY', default='4cn68iga94@**2x9vb1f', cast=str)


# Database

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'flask.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_CONNECT_OPTIONS = {}


# Flask-Mail configuration

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = config('MAIL_USERNAME', default='', cast=str)
MAIL_PASSWORD = config('MAIL_PASSWORD', default='', cast=str)
MAIL_USE_TLS = False
MAIL_USE_SSL = True


# Celery

CELERY_BROKER_URL = 'amqp://guest@localhost//'
result_backend = 'amqp://guest@localhost//'


# Logging

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        },
        'simple': {
            'format': '%(levelname)s [%(asctime)s] %(name)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'file-debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 16777216,  # 16MB
            'formatter': 'simple',
            'filename': '/var/log/flask/debug.log',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi', 'file-debug']
    }
})
