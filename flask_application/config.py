import os
import bcrypt
from flask.ext.mail import Mail

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = 'bigFatSecretsf00Bar$1'
    SITE_NAME = 'The Search Collective'
    SITE_ROOT_URL = 'localhost:5000'
    MEMCACHED_SERVERS = ['localhost:11211']
    SYS_ADMINS = ['jimmy@jimmymesta.com']
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    SECURITY_POST_LOGIN_VIEW= '/search'

    # Stripe

    SECRET_KEY= 'sk_test_wsjHditRLQ8BDh5FWBl1HHUB'
    #publishable_key = os.environ['PUBLISHABLE_KEY']
    PUBLISHABLE_KEY = 'pk_test_ilOGiFHlu0cP4oPxB2Jui5EH'

    DEFAULT_SMALL_AMOUNT = 525
    DEFAULT_SMALL_DESCRIPTION = "Small Plan"

    DEFAULT_LARGE_AMOUNT = 925
    DEFAULT_LARGE_DESCRIPTION = "Large Plan"



    # Mongodb support
    #MONGODB_DB = 'testing'
    #MONGODB_HOST = 'localhost'
    #MONGODB_PORT = 27017


    # Configured for GMAIL
    #MAIL_SERVER = 'localhost'
    #MAIL_PORT = 25
    #MAIL_USE_SSL = False
    #MAIL_USERNAME = 'datbikesite@gmail.com'
    #MAIL_PASSWORD = 'Redspin1!'
    #DEFAULT_MAIL_SENDER = 'datbikesite@gmail.com'
    #MAIL_DEBUG = True
    #MAIL_SUPRESS_SEND = True

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'jimmy.mesta@gmail.com'
    MAIL_PASSWORD = '671linden'
    MAIL_FAIL_SILENTLY=False

    # Flask-Security setup
    #SECURITY_LOGIN_WITHOUT_CONFIRMATION = False
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    #SECURITY_PASSWORD_SALT = bcrypt.gensalt()
    SECURITY_URL_PREFIX = '/auth'
    SECUIRTY_POST_LOGIN = '/search'
    SECURITY_TRACKABLE = True
    #SECURITY_CONFIRMABLE = True






class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SECURITY_CONFIRMABLE = False
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_PASSWORD_SALT = '$2a$16$PnnIgfMwkOjGX4SkHqSOPO'
    SECURITY_URL_PREFIX = '/auth'
    SECUIRTY_POST_LOGIN = '/search'
    SECURITY_TRACKABLE = True

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'datbikesite@gmail.com'
    MAIL_PASSWORD = 'Redspin1!'

    MONGO_DB = 'production'

    """secret_key= os.environ['SECRET_KEY']
    publishable_key = os.environ['PUBLISHABLE_KEY']

    DEFAULT_SMALL_AMOUNT = 525
    DEFAULT_SMALL_DESCRIPTION = "Small Plan"

    DEFAULT_LARGE_AMOUNT = 925
    DEFAULT_LARGE_DESCRIPTION = "Large Plan"""

class TestConfig(Config):
    SITE_ROOT_URL = 'http://localhost:5000'
    DEBUG = False
    TESTING = True

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'jimmy.mesta@gmail.com'
    MAIL_PASSWORD = '671linden'

class DevelopmentConfig(Config):
    SITE_ROOT_URL = 'http://localhost:5000'
    '''Use "if app.debug" anywhere in your code, that code will run in development code.'''
    DEBUG = True
    TESTING = True

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'jimmy.mesta@gmail.com'
    MAIL_PASSWORD = '671linden'

