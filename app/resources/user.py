from flask import request, jsonify, abort
from flask_restful import Resource, reqparse
from app import db

# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('userid', type=str, required=True, help='Tähä sun userid')

class User(Resource):
    def post(self):
        args = parser.parse_args(strict=True)
        return { 'userid': args.userid }


