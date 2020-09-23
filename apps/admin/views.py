from common.models.user import *
from flask_restful import Resource, Api, marshal
from flask import Blueprint
from .param_parse import *
from .marshals import *
from flask import request

admin_bp = Blueprint('admin', __name__)
admin_api = Api(admin_bp)


class AdminInfoView(Resource):

    def get(self):
        return {"code": 200, "data": marshal(request.current_user, admin_fields)}

    def put(self):
        req_val = UpdateAdminParse().parse_args()
        res = request.current_user.update(**req_val)
        if res['status'] == 'failure': return {"code": 202, "msg": res.get('msg', '')}
        else: return {"code": 200, "msg": "修改成功"}

    def post(self):
        req_val = AddAdminParse().parse_args()
        User.add(**req_val)
        return {"code": 200, "msg": "添加成功"}


class AdminLoginView(Resource):

    def post(self):
        req_val = AdminLoginParse().parse_args()
        res = User.check_password(**req_val, superuser=True)
        if res['status'] == 'failure': return {"code": 202, "msg": res['msg']}
        return {"code": 200, "token": res['user'].create_token()}


admin_api.add_resource(AdminInfoView, '/info')
admin_api.add_resource(AdminLoginView, '/login')

