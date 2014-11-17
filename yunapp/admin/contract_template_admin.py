from flask.ext.admin import BaseView, expose
from flask.ext import login

class ComtractTemplateAdminView(BaseView):

    def is_accessible(self):
        return login.current_user.is_authenticated()

    @expose('/')
    def index(self):
        return self.render('admin/contract_template.html')