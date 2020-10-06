from .views import *


def add_resource(api):
    api.add_resource(AddAdminView, '/admin/info')
    api.add_resource(AdminInfoView, '/admin/info/<int:admin_id>')
    api.add_resource(AdminLoginView, '/admin/login')
    api.add_resource(AdminListView, '/admin/superuser/list')
    api.add_resource(TokenGetAdminInfoView, '/admin/token/info')
