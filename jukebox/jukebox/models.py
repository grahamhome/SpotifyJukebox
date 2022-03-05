from . import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """
    A user of the application.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    can_create_users = db.Column(db.Boolean, default=False)
