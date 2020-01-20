from flask import current_app as app
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)