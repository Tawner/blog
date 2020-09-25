from common.models.article import *
from flask_restful import Resource, Api, marshal
from flask import Blueprint
from .param_parse import *
from .marshals import *
from flask import request

article_bp = Blueprint('article', __name__)
article_api = Api(article_bp)


class ArticleInfoView(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class ArticleListView(Resource):

    def get(self):
        pass


class ArticleStatusView(Resource):

    def put(self):
        pass




article_api.add_resource("/info", ArticleInfoView)
article_api.add_resource("/list", ArticleListView)

