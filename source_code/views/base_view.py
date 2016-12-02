from flask import request
from flask import render_template
from flask import jsonify
from flask import url_for
from flask import redirect
from flask import flash
from flask import session
from flask import abort
from flask import g
from flask.views import MethodView


class BaseView(MethodView):
    request = request
    session = session
    g = g

    def render_template(self, template_name, **kwargs):
        return render_template(template_name, **kwargs)

    def json_result(self, *args, **kwargs):
        return jsonify(*args, **kwargs)

    def url_for(self, *args, **kwargs):
        return url_for(*args, **kwargs)

    def redirect(self, *args, **kwargs):
        return redirect(*args, **kwargs)

    def flash(self, message, *args):
        return flash(message, *args)

    def abort(self, code):
        return abort(code)

    def __repr__(self):
        return '{}'.format(self.__class__)

    def __str__(self):
        return 'Class: {}. Table name: {}'.format(self.__class__,
                                                  self.__tablename__)
