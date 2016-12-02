from flask import g, request
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from database import db_session
from sqlalchemy import or_
from models import User, Post


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    user = User.verify_auth_token(email_or_token)
    if not user:
        user = User.query.filter_by(email=email_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


class GetAuthToken(Resource):

    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token(600)
        return {'token': token.decode('ascii'), 'duration': 600}, 200


class GetResorce(Resource):

    @auth.login_required
    def get(self):
        posts = db_session.query(Post).join(User).filter(User.id == g.user.id).all()
        posts = [{p.title: p.body} for p in posts]
        return {'email': g.user.email, 'posts': posts}, 200

    @auth.login_required
    def post(self):
        try:
            start = int(request.json.get('start'))
            end = int(request.json.get('end'))
            if end > start and start >= 0:
                posts = db_session.query(Post).join(User).filter(User.id == g.user.id).all()[start:end]
            else:
                return {'msg': 'incorrect diapason'}, 400
        except Exception:
            posts = db_session.query(Post).join(User).filter(User.id == g.user.id).all()
        posts = [{p.title: p.body} for p in posts]
        return {'email': g.user.email, 'posts': posts}, 200


class InsertRecord(Resource):

    @auth.login_required
    def post(self):
        title = request.json.get('title')
        body = request.json.get('body')
        if title is None or body is None:
            return {'msg': 'Not all arguments'}, 400
        post = Post(title=title, body=body, user_id=g.user.id)
        db_session.add(post)
        db_session.commit()
        return {'email': g.user.email, 'title': title, 'body': body}, 200


class SearchRecord(Resource):

    @auth.login_required
    def post(self):
        search = request.json.get('search')
        posts = db_session.query(Post).join(User).filter(User.id == g.user.id).\
            filter(or_(Post.title.like("%{}%".format(search)), Post.body.like("%{}%".format(search)))).all()
        posts = [{p.title: p.body} for p in posts]
        return {'email': g.user.email, 'posts': posts}


class NewUser(Resource):

    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')
        if email is None or password is None:
            return {'msg': 'Not all arguments'}, 400
        if User.query.filter_by(email=email).first() is not None:
            return {'msg': 'User is exist'}, 400
        user = User(email=email)
        user.hash_password(password)
        db_session.add(user)
        db_session.commit()
        return {'email': user.email}, 200


class GetUser(Resource):

    def get(self, id):
        user = User.query.get(id)
        if not user:
            return {'msg': 'User is not exist'}, 400
        return {'email': user.email}, 200
