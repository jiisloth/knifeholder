from flask import request, jsonify, abort
from flask_restful import Resource, reqparse
from app.models import Games, Players
import uuid
from app import db

# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('gameid', type=str, required=True, help='Please give gameid')
parser.add_argument('name', type=str, required=True, help='Please give name')
parser.add_argument('team', type=str, required=False, help='You can include team, A or B')


class JoinGame(Resource):
    def post(self):
        args = parser.parse_args(strict=True)
        players = Players.query.filter_by(gameid=args.gameid).all()
        games = Games.query.filter_by(gameid=args.gameid).all()
        if not games:
            return 400

        if len(players) >= 4:
            return 400

        flag = True
        while True:
            playerid = str(uuid.uuid4())
            for player in players:
                if playerid == player.playerid:
                   flag = False
            if flag:
                break
        A = 0
        B = 0
        for player in players:
            if player.team == "A":
                A += 1
            else:
                B += 1

        if args.team:
            if args.team == "A" and A < 2:
                team = "A"
            elif args.team == "B" and B < 2:
                team = "B"
            else:
                return 400
        else:
            if A < 2:
                team = "A"
            else:
                team = "B"

        sub = Players(
            playerid=playerid,
            name=args.name,
            game=args.gameid,
            team=team
        )
        db.session.add(sub)
        db.session.commit()
        if len(players) < 3:
            status = "waiting for " + str(3 - len(players)) + " players"
        else:
            status = "ready"
        return {'playerid': playerid, 'status': status}
