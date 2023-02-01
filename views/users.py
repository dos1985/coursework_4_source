# Представление для пользователя
from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service
from utils import auth_required, get_email

algo = 'HS256'
user_ns = Namespace('user')


@user_ns.route('/')
class UsersView(Resource):
    """Класс пользователей"""
    @auth_required
    def get(self):
        """
        Вывод профиля пользователя
        """
        email = get_email()
        rs = user_service.get_one(email)
        res = UserSchema().dump(rs)
        return res, 200

    @auth_required
    def patch(self):
        """
        Обновление профиля пользователя
        """
        req_json = request.json
        email = get_email()
        rs = user_service.get_one(email)
        if "id" not in req_json:
            req_json["id"] = rs.id
        user_service.update(req_json)
        return "", 200


@user_ns.route('/password/')
class UserView(Resource):
    @auth_required
    def put(self):
        """Обновление пароля"""
        req_json = request.json
        password_1 = req_json['old_password']
        password_2 = req_json['new_password']
        email = get_email()
        if user_service.check_password(email, password_1):
            passwd_new = user_service.get_hash(password_2)
            rs = user_service.get_one(email)
            data = {'id': rs.id, 'password': passwd_new}
            user_service.update(data)
        return "", 200


