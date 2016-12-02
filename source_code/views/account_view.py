from flask_login import login_required
from views.base_view import SuperUserView
from forms.account_form import AccountForm
from models.db import User, Employee
from database import db_session


class AccountView(SuperUserView):

    @login_required
    def get(self):
        user_employee = db_session.query(User, Employee).filter(User.id == Employee.id).\
            filter(User.id == self.g.user.get_id()).one()
        param = {
            'page_name': 'Account',
            'search_false': True,
            'first_name': user_employee[1].first_name,
            'last_name': user_employee[1].last_name,
            'address': user_employee[1].address,
            'city': user_employee[1].city,
            'hire_date': user_employee[1].hire_date,
            'base_salary': user_employee[1].base_salary,
            'phone': user_employee[1].phone,
        }
        return self.render_template('account.html', form=AccountForm(), **param)

    @login_required
    def post(self):
        first_name = self.request.form.get('first_name')
        last_name = self.request.form.get('last_name')
        address = self.request.form.get('address')
        city = self.request.form.get('city')
        phone = self.request.form.get('phone')
        hire_date = self.request.form.get('hire_date')
        base_salary = self.request.form.get('base_salary')
        update = {
            'first_name': first_name,
            'last_name': last_name,
            'address': address,
            'city': city,
            'phone': phone,
        }
        db_session.query(Employee).filter(Employee.user_id == self.g.user.get_id()).update(update)
        db_session.commit()
        param = {
            'page_name': 'Account',
            'search_false': True,
            'first_name': first_name,
            'last_name': last_name,
            'address': address,
            'city': city,
            'hire_date': hire_date,
            'base_salary': base_salary,
            'phone': phone,
        }
        return self.render_template('account.html', form=AccountForm(), **param)
