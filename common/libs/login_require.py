from flask import request, abort


def AdminLoginRequired(func):
    def wrapper(self, *args, **kwargs):
        if request.current_user and request.current_user.is_super:
            return func(self, *args, **kwargs)
        else:
            abort(401)
    return wrapper


def UserLoginRequired(func):
    def wrapper(self, *args, **kwargs):
        if request.current_user and not request.current_user.is_super:
            return func(self, *args, **kwargs)
        else:
            abort(401)
    return wrapper


def UserOrAdminLoginRequired(func):
    def wrapper(self, *args, **kwargs):
        if request.current_user:
            return func(self, *args, **kwargs)
        else:
            abort(401)
    return wrapper



