from models.db import User
from database import db_session
from utils import hashing_sha224


def get_activated_user(email, password):
    return User.query.filter_by(email=email, password=hashing_sha224(password)).first()


def get_user_by_name(email=None):
    return User.query.filter_by(email=email).first()


def add_user(email=None, password=None, ip=''):
    new_user = User(email=email, password=hashing_sha224(password))
    db_session.add(new_user)
