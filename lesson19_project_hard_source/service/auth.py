from flask import abort
import jwt
import datetime
import calendar

from helpers.constants import SECRET, ALGO
from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refresh=False):
        """
        Метод генерирует токены по username и password
        """
        user = self.user_service.get_by_username(username)
        if user is None:
            abort(400)
        if not is_refresh:
            if not self.user_service.comprare_passwords(user.password, password):
                abort(400)
        data = {
            "username": username,
            "role": user.role
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, SECRET, algoritms=[ALGO])

        days30 = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        data["exp"] = calendar.timegm(days30.timetuple())
        refresh_token = jwt.encode(data, SECRET, algoritms=[ALGO])

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def aprove_refresh_token(self, token):
        """
        Метод генерирует токены по refresh_token
        """
        data = jwt.decode(jwt=token, key=SECRET, algoritms=[ALGO])
        username = data.get("username")
        return self.generate_tokens(username, None, is_refresh=True)
