from flask_login import login_required
from views.base_view import BaseView


class HelloWordView(BaseView):

    @login_required
    def get(self):
        return self.render_template(template_name='hello.html')
