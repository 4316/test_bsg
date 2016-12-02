from flask import Flask
from flask_restful import Api
from database import db_session
from resources.token_resource import (
    GetResorce,
    GetAuthToken,
    InsertRecord,
    SearchRecord,
    NewUser,
    GetUser,
)


app = Flask(__name__)

app.config.from_pyfile('config.py')
api = Api(app)
api.add_resource(NewUser, '/api/users', endpoint='new_user')
api.add_resource(GetUser, '/api/users/<int:id>', endpoint='get_user')
api.add_resource(GetAuthToken, '/api/token', endpoint='get_token')
api.add_resource(GetResorce, '/api/resource', endpoint='get_resource')
api.add_resource(InsertRecord, '/api/insert', endpoint='insert')
api.add_resource(SearchRecord, '/api/search', endpoint='search')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
