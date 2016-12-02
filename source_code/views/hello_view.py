from flask_login import login_required
from views.base_view import BaseView


class HelloView(BaseView):

    @login_required
    def get(self, name=None):
        return self.render_template('hello.html', name=name)
