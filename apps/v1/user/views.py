from common.models.user import *
from flask_restful import Resource, marshal
from .param_parse import *
from .marshals import *
from flask import request


class UserInfoView(Resource):

    def get(self):
        return {"code": 200, "data": marshal(request.current_user, user_fields)}

    def put(self):
        req_val = UpdateUserParse().parse_args()
        res = request.current_user.update(**req_val)
        if res['status'] == 'failure': return {"code": 202, "msg": res.get('msg', '')}
        else: return {"code": 200, "msg": "修改成功"}


class UserLoginView(Resource):

    def post(self):
        req_val = UserLoginParse().parse_args()
        res = User.check_password(**req_val)
        if res['status'] == 'failure': return {"code": 202, "msg": res['msg']}
        return {"code": 200, "token": res['user'].create_token()}


class UserSignUpView(Resource):

    def post(self):
        req_val = AddUserParse().parse_args()
        res = User.add(**req_val)
        if res['status'] == "failure":
            return {"code": 202, "msg": res['msg']}
        else:
            return {"code": 200, "msg": "添加成功"}


