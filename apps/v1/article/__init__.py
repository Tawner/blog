from .views import *


def add_resource(api):
    api.add_resource(ArticleInfoView, '/article/info/<int:article_id>')

