import os

from srblib import SrbJson

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_dance.contrib.google import make_google_blueprint

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

db = SQLAlchemy()
mail = Mail()

class Config:
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    conf = SrbJson('~/.config/iblog/config.json')
    SQLALCHEMY_DATABASE_URI = conf.get('SQLALCHEMY_DATABASE_URI','')
    SECRET_KEY = conf.get('SECRET_KEY','its_a_secret_i_wont_tell_you')
    MAIL_USERNAME = conf.get('MAIL_USERNAME','srbcheema1.iblog@gmail.com')
    MAIL_PASSWORD = conf.get('MAIL_PASSWORD','')
    GOOGLE_OAUTH_CLIENT_ID = conf.get('GOOGLE_OAUTH_CLIENT_ID','')
    GOOGLE_OAUTH_CLIENT_SECRET = conf.get('GOOGLE_OAUTH_CLIENT_SECRET','')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from iblog.users.routes import users
    from iblog.posts.routes import posts
    from iblog.main.routes import main
    from iblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    google_bp = make_google_blueprint(
        offline=True,
        redirect_url='/google_login',
        scope=[
            "https://www.googleapis.com/auth/plus.me",
            "openid https://www.googleapis.com/auth/userinfo.email",
        ]
    )
    app.register_blueprint(google_bp, url_prefix="/google_login")

    return app

