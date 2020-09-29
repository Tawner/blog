from flask import request, abort


class AdminLoginRequired:

    def __init__(self, func):
        self._func = func

    def __call__(self, *args, **kwargs):
        if request.current_user and request.current_user.is_super:
            return self._func(*args, **kwargs)
        else:
            abort(401)


class UserLoginRequired:

    def __init__(self, func):
        self._func = func

    def __call__(self, *args, **kwargs):
        if request.current_user and not request.current_user.is_super:
            return self._func(*args, **kwargs)
        else:
            abort(401)


class UserOrAdminLoginRequired:
    def __init__(self, func):
        self._func = func

    def __call__(self, *args, **kwargs):
        if request.current_user:
            return self._func(*args, **kwargs)
        else:
            abort(401)
