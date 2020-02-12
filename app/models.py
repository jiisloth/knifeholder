from flask import current_app as app
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gameid = db.Column(db.String(256))
    state = db.Column(db.String(256))
    mode = db.Column(db.String(256))

class Players(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playerid = db.Column(db.String(256))
    name = db.Column(db.String(256))
    game = db.Column(db.String(256))
    team = db.Column(db.String(256))

class Teams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(256))
    team = db.Column(db.String(256))
    score = db.Column(db.String(256))

class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(256))
    owner = db.Column(db.String(256))
    suit = db.Column(db.String(256))
    value = db.Column(db.String(256))

