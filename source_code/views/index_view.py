from flask_login import login_required
from views.base_view import BaseView


class IndexView(BaseView):

    @login_required
    def get(self):
        return self.render_template('index.html', page_name='Index')
