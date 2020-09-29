from common.models.models import User
from flask_restful import Resource, marshal
from .param_parse import *
from .marshals import *
from common.libs.login_require import *


# 前台接口
class UserInfoView(Resource):
    """获取、修改当前用户的信息"""
    @UserLoginRequired
    def get(self):
        return {"code": 200, "data": marshal(request.current_user, user_fields)}

    @UserLoginRequired
    def put(self):
        req_val = UpdateUserParse().parse_args()
        res = request.current_user.update(**req_val)
        if res['status'] == 'failure': return {"code": 202, "msg": res.get('msg', '')}
        else: return {"code": 200, "msg": "修改成功"}


class UserLoginView(Resource):
    """登陆接口"""
    def post(self):
        req_val = UserLoginParse().parse_args()
        res = User.check_password(**req_val)
        if res['status'] == 'failure': return {"code": 202, "msg": res['msg']}
        return {"code": 200, "token": res['user'].create_token()}


class UserSignUpView(Resource):
    """注册接口"""
    def post(self):
        req_val = AddUserParse().parse_args()
        res = User.add(**req_val)
        if res['status'] == "failure":
            return {"code": 202, "msg": res['msg']}
        else:
            return {"code": 200, "msg": "添加成功"}


# 后台接口
class UserListAdminView(Resource):
    """获取用户列表"""
    @AdminLoginRequired
    def get(self):
        # 参数校验
        req_val = UserListAdminParse().parse_args()

        # 数据查询
        query_args = [User.is_delete == 0, User.superuser == 0]
        if req_val.get("word", None): query_args.append(User.nickname.like("%" + req_val['word'] + "%"))
        users = User.query.filter(*query_args).paginate(req_val['page'], req_val['rows'])

        # 数据整形
        page_data = {"page": users.page, "rows": req_val['rows'], "total_page": users.pages}
        data = marshal(users, user_fields)
        return {"code": 200, "data": data, "page_data": page_data}


class UserInfoAdminView(Resource):
    """后台获取、修改、删除前台用户接口"""
    @AdminLoginRequired
    def get(self, user_id):
        user = User.query.filter(User.id == user_id, User.is_delete == 0, User.superuser == 0).first_or_404()
        return {"code": 200, "data": marshal(user, user_fields)}

    @AdminLoginRequired
    def put(self, user_id):
        # 参数校验
        req_val = UserInfoAdminUpdateParse().parse_args()

        # 获取数据并修改
        user = User.query.filter(User.id == user_id, User.is_delete == 0, User.superuser == 0).first_or_404()
        user.update(**req_val)
        return {"code": 200, "msg": "修改成功"}

    @AdminLoginRequired
    def delete(self, user_id):
        user = User.query.filter(User.id == user_id, User.is_delete == 0, User.superuser == 0).first_or_404()
        user.delete()
        return {"code": 200, "msg": "删除成功"}



