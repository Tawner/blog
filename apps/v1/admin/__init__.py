from .views import *


def add_resource(api):
    api.add_resource(AdminInfoView, '/admin/info')
    api.add_resource(AdminLoginView, '/admin/login')
