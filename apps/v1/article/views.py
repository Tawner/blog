from common.models.models import Article
from flask_restful import Resource, marshal
from .param_parse import *
from .marshals import *
from sqlalchemy import or_


# 前台接口
class ArticleListView(Resource):
    """获取文章列表"""
    def get(self):
        req_val = ArticleListParse().parse_args()

        query_args = [Article.is_delete == 0, Article.category_id == req_val['category'], Article.published == 1]
        if req_val.get("word", None): query_args.append(or_(
            Article.title.like('%' + req_val['word'] + '%'),
            Article.content.like('%' + req_val['word'] + '%')
        ))
        article = Article.query.filter(*query_args).order_by(Article.create_time.desc()).paginate(req_val['page'], req_val['rows'])
        page_data = {"page": article.page, "rows": req_val['rows'], "total_page": article.pages}
        return {"code": 200, "data": marshal(article.items, article_info_field), "page_data": page_data}


class ArticleInfoView(Resource):
    """获取文章信息"""
    def get(self, article_id):
        article = Article.query.filter(Article.id == article_id, Article.is_delete == 0).first_or_404()
        return {"code": 200, "data": marshal(article, article_info_field)}


# 后台接口
class AddArticleAdminView(Resource):
    def post(self):
        pass


class ArticleInfoAdminView(Resource):

    def get(self, article_id):
        article = Article.query.filter(Article.id == article_id, Article.is_delete == 0).first_or_404()
        return {"code": 200, "data": marshal(article, article_info_admin_field)}

    def put(self, article_id):
        article = Article.query.filter(Article.id == article_id, Article.is_delete == 0).first_or_404()

        return {"code": 200, "msg": "修改成功"}

    def delete(self, article):
        pass






