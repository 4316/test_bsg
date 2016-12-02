from flask import current_app
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired,
)
from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String(50), index=True)
    password_hash = Column(String(64), nullable=False)

    def __init__(self, email=None, password=None):
        self.email = email
        self.password = password

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user

    def __str__(self):
        return self.email

    @classmethod
    def get_users_count(self):
        return self.query.count()


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(10), unique=True, nullable=False)
    body = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    def __init__(self, title=None, body=None, user_id=None):
        self.title = title
        self.body = body
        self.user_id = user_id
