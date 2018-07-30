import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'hard to guess string'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_MAIL_SUBJECT_PREFIX = '[Flask]'
    FLASK_MAIL_SENDER = 'Flask Admin <1933592511@qq.com>'
    FLASK_ADMIN = '1933592511@qq.com'
    FLASK_POSTS_PER_PAGE=10
    FLASK_FOLLOWERS_PER_PAGE=10
    FLASK_COMMENTS_PER_PAGE=10

    @staticmethod
    def init_app(app):
        pass
    
class DevelopmentConfig(Config):
    DEBUG=True
    MAIL_SERVER='smtp.qq.com'
    MAIL_PORT=465
    MAIL_USE_TLS=False
    MAIL_USE_SSL=True
    MAIL_USERNAME = '1933592511@qq.com'
    MAIL_PASSWORD = 'kbyolqemxapheccd'
    SQLALCHEMY_DATABASE_URI=os.environ.get('DEV_DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'data-dev.sqlite')

class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI=os.environ.get('DEV_DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'data-test.sqlite')
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI=os.environ.get('DEV_DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}