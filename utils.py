# описание декоратор авторизации и необходимые функции
import jwt
from flask import request
from flask_restx import abort
from constants import PWD_HASH_SALT

algo = 'HS256'


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, PWD_HASH_SALT, algorithms=[algo])
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, **kwargs)
    return wrapper


# Получение email из токенв
def get_email():
    data = request.headers['Authorization']
    token = data.split("Bearer ")[-1]
    d_token = jwt.decode(token, PWD_HASH_SALT, algorithms=[algo])
    email = d_token['email']
    return email