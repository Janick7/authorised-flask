from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask_login import LoginManager
from os import path
# import pymysql

db = SQLAlchemy()
ENV = 'dev' # 'dev' or 'prod'
DB_USER = ''
DB_PASS = ''
DB_NAME = 'webapp.db'

def webapp():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fitoz75lffjzegdhjf'

    if ENV == 'dev':
        app.debug = True
        conn = f'sqlite:///{DB_NAME}'
        # conn = sqlite3.connect(DB_NAME)

    if ENV == 'prod':
        app.debug = False
        conn = 'mysql + pymysql://' + DB_USER + ':(' + DB_PASS + ')@localhost:3306/' + DB_NAME[:-3]

    app.config['SQLALCHEMY_DATABASE_URI'] = conn
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


    from views import views
    from auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    from models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if ENV == 'dev':
        if not path.exists(DB_NAME):
            db.create_all(app=app)
            print('Created Database!')
