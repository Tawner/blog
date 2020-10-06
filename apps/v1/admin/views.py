from common.libs.login_require import *
from common.models.models import User
from flask_restful import Resource, marshal
from .param_parse import *
from .marshals import *
from flask import request


class AddAdminView(Resource):
    """添加管理员"""
    @AdminLoginRequired
    def post(self):
        req_val = AddAdminParse().parse_args()
        res = User.add(**req_val)
        if res['status'] == "failure":
            return {"code": 202, "msg": res['msg']}
        else:
            return {"code": 200, "msg": "添加成功"}
        

class TokenGetAdminInfoView(Resource):
    def get(self):
        return {"code": 200, "data": marshal(request.current_user, admin_fields)}


class AdminInfoView(Resource):
    """修改、获取、删除管理员"""
    @AdminLoginRequired
    def get(self, admin_id):
        # 数据查询
        admin = User.query.filter(User.id == admin_id, User.superuser == 1, User.is_delete == 0).first_or_404()

        # 数据整形
        data = marshal(admin, admin_fields)
        return {"code": 200, "data": data}

    @AdminLoginRequired
    def put(self, admin_id):
        # 参数校验
        req_val = UpdateAdminParse().parse_args()

        # 数据查询与修改
        admin = User.query.filter(User.id == admin_id, User.is_super == 1, User.is_delete == 0).first_or_404()
        res = admin.update(**req_val)

        r = {"code": 202, "msg": res.get('msg', '')} if res['status'] == 'failure' else {"code": 200, "msg": "修改成功"}
        return r

    @AdminLoginRequired
    def delete(self, admin_id):
        admin = User.query.filter(User.id == admin_id, User.is_super == 1, User.is_delete == 0).first_or_404()
        admin.delete()
        return {"code": 200, "msg": "删除成功"}


class AdminListView(Resource):
    """获取管理员列表"""
    @AdminLoginRequired
    def get(self):
        # 参数校验
        req_val = AdminListParse().parse_args()

        # 数据查询
        query_args = [User.is_delete == 0, User.superuser == 1]
        if req_val.get('word', None): query_args.append(User.nickname.like('%' + req_val['word'] + '%'))
        users = User.query.filter(*query_args).paginate(req_val['page'], req_val['rows'])

        # 数据整形
        page_data = {"page": users.page, "rows": req_val['rows'], "total_page": users.pages}
        data = marshal(users.items, admin_fields)
        return {"code": 200, "data": data, "page_data": page_data}


class AdminLoginView(Resource):
    """登陆"""
    def post(self):
        # 参数校验
        req_val = AdminLoginParse().parse_args()

        # 登陆验证
        res = User.check_password(**req_val, superuser=True)
        r = {"code": 202, "msg": res['msg']}if res['status'] == 'failure' else {"code": 200, "token": res['user'].create_token()}
        return r




