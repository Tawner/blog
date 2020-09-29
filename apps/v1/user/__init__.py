from .views import *


def add_resource(api):
    api.add_resource(UserInfoView, '/user/info')
    api.add_resource(UserLoginView, '/user/login')
    api.add_resource(UserSignUpView, '/user/sign_up')
    api.add_resource(UserListAdminView, '/admin/user/list')
    api.add_resource(UserInfoAdminView, '/admin/user/info/<int:user_id>')

