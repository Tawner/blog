from common.models.article import *
from flask_restful import Resource, Api, marshal
from flask import Blueprint
from .param_parse import *
from .marshals import *
from flask import request
from flask_restful import reqparse


class ArticleInfoView(Resource):

    def get(self, article_id):
        parse = reqparse.RequestParser()
        parse.add_argument("id", type=int, required=True)
        req_val = parse.parse_args()
        return req_val

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






