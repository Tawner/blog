from flask import Blueprint
from flask_restful import Api
from . import admin, article, category, user, upload

api_v1_bp = Blueprint("api_v1", __name__)
api = Api(api_v1_bp)

# 注册url
admin.add_resource(api)
user.add_resource(api)
upload.add_resource(api)
article.add_resource(api)
# category.add_resource(api)


