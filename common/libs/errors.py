from flask import jsonify, current_app
from werkzeug.http import HTTP_STATUS_CODES


def api_abort(code, message=None, **kwargs):
    if message is None:
        message = HTTP_STATUS_CODES.get(code, '')

    response = jsonify(message=message, **kwargs)
    return response, code


def error_handler(app):
    @app.errorhandler(400)
    def bad_request(e):
        return api_abort(400)

    @app.errorhandler(403)
    def forbidden(e):
        return api_abort(403)

    @app.errorhandler(404)
    def database_not_found_error_handler(e):
        return api_abort(404)

    @app.errorhandler(405)
    def method_not_allowed(e):
        return api_abort(405, message='The method is not allowed for the requested URL.')

    @app.errorhandler(500)
    def internal_server_error(e):
        return api_abort(500, message='An internal server error occurred.')

    # The default_error_handler function as written above will not return any response if the Flask application
    # is running in DEBUG mode.
    @app.errorhandler(Exception)
    def default_error_handler(e):
        message = 'An unhandled exception occurred. -> {}'.format(str(e))
        current_app.logger.error(message)
        # if not settings.FLASK_DEBUG:
        return api_abort(500, message=message)


def invalid_token():
    response, code = api_abort(401)
    return response, code


# class ValidationError(ValueError):
#     pass

# 简单列了一些，别的类型自己可以根据需要扩展补充
# from itpms.api.v1.order import api as order_api
# @order_api.errorhandler(ValidationError)
# def validation_error(e):
#     return api_abort(400, e.args[0])



