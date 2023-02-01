from flask import request
from flask_restx import Namespace, Resource, abort

from implemented import user_service, auth_service


auth_ns: Namespace = Namespace('auth')


@auth_ns.route('/register/')
class AuthRegisterView(Resource):
    def post(self):
        req_json = request.json
        email = req_json.get('email')
        password = req_json.get('password')
        if not email or not password:
            abort(400, "Both email and password are required")

        try:
            user_service.create(req_json)
        except Exception as e:
            abort(500, f"Error creating user: {str(e)}")

        return "User created", 201


@auth_ns.route('/login/')
class AuthLoginView(Resource):
    def post(self):
        req_json = request.get_json()
        if not req_json or not all(key in req_json for key in ['email', 'password']):
            abort(400, 'Bad Request: Missing email and/or password')

        email = req_json.get('email')
        password = req_json.get('password')

        result = user_service.auth_user(email, password)
        if result:
            return result, 200
        else:
            abort(401, 'Unauthorized: Invalid email and/or password')

    def put(self):
        req_json = request.get_json()
        if not req_json or 'refresh_token' not in req_json:
            abort(400, 'Bad Request: Missing refresh_token')

        result = user_service.check_token(req_json['refresh_token'])
        if result:
            return result, 200
        else:
            abort(401, 'Unauthorized: Invalid refresh_token')
