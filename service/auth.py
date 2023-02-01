from typing import Optional, Dict

from flask_restx import abort
import jwt

from config import Config
from dao.model.user import User
from service.user import UserService


class AuthService:
    user_service: UserService

    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    def generate_tokens(self, username: str, password: Optional[str], is_refresh: bool = False) -> Dict[str, str]:
        user: User = self.user_service.get_by_name(username)

        if user is None:
            raise abort(404)

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                raise abort(400)

        data: Dict[str, str] = {
            'username': user.username,
            'role': user.role
        }

        access_token: str = self.user_service.generate_access_token(data)
        refresh_token: str = self.user_service.generate_refresh_token(data)

        return {'access_token': access_token,
                'refresh_token': refresh_token}

    def approve_refresh_taken(self, refresh_token: str):
        data: Dict[str, str] = jwt.decode(jwt=refresh_token, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGO)
        username: Optional[str] = data.get('username', None)
        if username is None:
            raise abort(400)
        return self.generate_tokens(username, None, is_refresh=True)