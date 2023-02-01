from typing import Dict, Tuple, Any, Optional, Union

from flask import request
from flask_restx import Namespace, Resource

from implemented import auth_service


auth_ns: Namespace = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):

    def post(self) -> Tuple[Union[Dict[str, str], str], int]:
        data: Dict[str, Any] = request.json

        username: Optional[str] = data.get('username', None)
        password: Optional[str] = data.get('password', None)

        if None in [username, password]:
            return '', 401

        return auth_service.generate_tokens(username, password), 200

    def put(self) -> Tuple[Dict[str, str], int]:
        data: Dict[str, Any] = request.json

        token: str = data.get('refresh_token')
        return auth_service.approve_refresh_taken(token), 200