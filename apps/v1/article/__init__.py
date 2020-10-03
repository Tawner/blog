from .views import *


def add_resource(api):
    api.add_resource(ArticleListView, '/article/list')
    api.add_resource(ArticleInfoView, '/article/info/<int:article_id>')
    api.add_resource(AddArticleAdminView, '/admin/article/info')
    api.add_resource(ArticleInfoAdminView, '/admin/article/info/<int:article_id>')
    api.add_resource(ArticleListAdminView, '/admin/article/list')

