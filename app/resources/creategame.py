from flask import request, jsonify, abort
from flask_restful import Resource, reqparse
from app.models import Games
import uuid
from app import db


class CreateGame(Resource):
    def get(self):
        games = Games.query.all()
        flag = True
        while True:
            gameid = str(uuid.uuid4())
            for games in games:
                if gameid == games.gameid:
                   flag = False
            if flag:
                break

        sub = Games(
            gameid=gameid,
            state="waiting_players",
            mode=""
        )
        db.session.add(sub)
        db.session.commit()

        return {'gameid': gameid}
