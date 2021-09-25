from flask_login import UserMixin
from application import db

class User(db.Model, UserMixin):
    __tablename__ ='user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))