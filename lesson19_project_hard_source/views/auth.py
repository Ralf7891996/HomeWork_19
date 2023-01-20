from flask import request
from flask_restx import Resource, Namespace

from implemented import auth_service

auth_ns = Namespace('auth')

#Добавляем эндпоинты аутентификации
@auth_ns.route('/')
class AuthViews(Resource):
    def post(self):
        data_request = request.json
        username = data_request.get("username", None)
        password = data_request.get("password", None)
        if None in [username, password]:
            return 400
        tokens = auth_service.generate_tokens(username, password)
        return tokens, 201

    def put(self):
        data_request = request.json
        token = data_request("refresh_token")
        if token is None:
            return 400
        tokens = auth_service.aprove_refresh_token(token)
        return tokens, 201