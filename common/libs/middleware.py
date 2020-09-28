from flask import request
from common.models.user import User


def middleware_register(app):

    @app.before_request
    def identity_check():
        path = request.path
        if path.split('/')[-1].isdigit():
            path = '/'.join(path.split('/')[:-1]) + '/'

        # token校验
        token = request.headers.get('Authorization', None)
        request.current_user = None
        if token:
            user = User.check_token(token)
            if user['status'] == "success":
                request.current_user = user['user']
            else:
                return {"code": 301, "msg": user['msg']}

        # 白名单
        if path in app.config['WHITE_URL']: return None

        # 接口判断
        if path.startswith('/api/user'):
            return None if request.current_user and request.current_user.superuser == 0 else {"code": 301, "msg": "token校验失败"}
        elif path.startswith('/api/admin'):
            return None if request.current_user and request.current_user.superuser == 1 else {"code": 301, "msg": "token校验失败"}
        else:
            return None

