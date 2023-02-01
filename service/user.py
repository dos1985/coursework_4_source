import datetime
import hashlib
import calendar

import jwt

from dao.user import UserDAO
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS



class UserService:
    dao: UserDAO

    def __init__(self, dao: UserDAO) -> None:
        self.dao = dao

    def get_one(self, user_id: int) -> User:
        return self.dao.get_one(user_id)

    def get_by_name(self, username: str) -> User:
        return self.dao.get_by_name(username)

    def get_all(self) -> List[User]:
        return self.dao.get_all()

    def update(self, user_id: int, data: Dict[str, Any]) -> User:
        user_by_id: User = self.dao.get_one(user_id)
        for k, v in data.items():
            if k == "password":
                setattr(user_by_id, k, self.encode_password(v))
            else:
                setattr(user_by_id, k, v)
        return self.dao.update(user_by_id)

    def create(self, data: Dict[str, Any]) -> User:

        encoded_password: str = self.encode_password(data['password'])
        data['password'] = encoded_password

        user: User = User(**data)
        return self.dao.create(user)

    def delete(self, user_id: int) -> None:
        self.dao.delete(user_id)


    def get_hash(self, password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")

    def get_tokens(self, data):
        date_time = datetime.datetime.utcnow()

        min30 = date_time + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, PWD_HASH_SALT, algorithm='HS256')

        days130 = date_time + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, PWD_HASH_SALT, algorithm='HS256')
        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return tokens

    def auth_user(self, email, password):
        user = self.dao.get_one_by_email(email)
        if not user:
            return "Нет пользователя с таким логином", 401

        passwd_new = self.get_hash(password)
        if passwd_new != user.password:
            return "Неверный пароль", 401

        data = {
            "email": user.email
        }
        return self.get_tokens(data)

    def check_token(self, token):
        try:
            data = jwt.decode(token, PWD_HASH_SALT, algorithms='HS256')
            return self.get_tokens(data)
        except Exception as e:
            raise e

    def check_password(self, email, password):
        user = self.dao.get_one_by_email(email)
        passwd_new = self.get_hash(password)
        if passwd_new != user.password:
            return "Неверный старый пароль", 401
        return True