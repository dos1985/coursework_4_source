from typing import Dict, Tuple, Any, List

from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema, User
from decorator import admin_required
from implemented import user_service

user_ns: Namespace = Namespace('users')
user_schema: UserSchema = UserSchema()
users_schema: UserSchema = UserSchema(many=True)


@user_ns.route('/')
class UsersView(Resource):

    @admin_required
    def get(self) -> Tuple[List[Dict[str, Any]], int]:
        all_users: List[User] = user_service.get_all()
        return users_schema.dump(all_users), 200

    def post(self) -> Tuple[str, int, Dict[str, str]]:
        req_json: Dict[str, Any] = request.json
        user: User = user_service.create(req_json)
        return "", 201, {"location": f"/users/{user.id}"}


@user_ns.route('/<int:uid>')
class UserView(Resource):
    @admin_required
    def get(self, uid: int) -> Tuple[Dict[str, Any], int]:
        user: User = user_service.get_one(uid)
        return user_schema.dump(user), 200

    @admin_required
    def put(self, uid: int) -> Tuple[str, int]:
        req_json: Dict[str, Any] = request.json
        user_service.update(uid, req_json)
        return "", 204

    @admin_required
    def delete(self, uid: int) -> Tuple[str, int]:
        user_service.delete(uid)
        return "", 204