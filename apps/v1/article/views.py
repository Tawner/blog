from common.models.models import Article, db
from flask_restful import Resource, marshal
from .param_parse import *
from .marshals import *
from sqlalchemy import or_
from common.libs.login_require import *


# 前台接口
class ArticleListView(Resource):
    """获取文章列表"""
    def get(self):
        req_val = ArticleListParse().parse_args()

        query_args = [Article.is_delete == 0,  Article.published == 1]
        if req_val.get('category', None): query_args.append(Article.category_id == req_val['category'])
        if req_val['recom'] != 0: query_args.append(Article.recom == req_val['recom'] - 1)
        if req_val.get("word", None): query_args.append(or_(
            Article.title.like('%' + req_val['word'] + '%'),
            Article.content.like('%' + req_val['word'] + '%')
        ))
        article = Article.query.filter(*query_args).order_by(Article.create_time.desc()).paginate(req_val['page'], req_val['rows'])
        page_data = {"page": article.page, "rows": req_val['rows'], "total_page": article.pages}
        return {"code": 200, "data": marshal(article.items, article_list_field), "page_data": page_data}


class ArticleInfoView(Resource):
    """获取文章信息"""
    def get(self, article_id):
        article = Article.query.filter(Article.id == article_id, Article.is_delete == 0).first_or_404()
        return {"code": 200, "data": marshal(article, article_info_field)}


# 后台接口
class AddArticleAdminView(Resource):
    """提交文章"""
    @AdminLoginRequired
    def post(self):
        req_val = AddArticleParse().parse_args()

        article = Article(**req_val)
        db.session.add(article)
        db.session.commit()
        return {"code": 200, "msg": "添加成功"}


class ArticleInfoAdminView(Resource):
    """获取、修改、删除文章"""
    @AdminLoginRequired
    def get(self, article_id):
        article = Article.query.filter(Article.id == article_id, Article.is_delete == 0).first_or_404()
        return {"code": 200, "data": marshal(article, article_info_admin_field)}

    @AdminLoginRequired
    def put(self, article_id):
        req_val = UpdateArticleParse().parse_args()
        article = Article.query.filter(Article.id == article_id, Article.is_delete == 0).first_or_404()
        article.set_attrs(req_val)
        db.session.commit()
        return {"code": 200, "msg": "修改成功"}

    @AdminLoginRequired
    def delete(self, article_id):
        article = Article.query.filter(Article.id == article_id, Article.is_delete == 0).first_or_404()
        article.delete()
        return {"code": 200, "msg": "删除成功"}


class ArticleListAdminView(Resource):
    """获取文章列表"""
    @AdminLoginRequired
    def get(self):
        req_val = ArticleListAdminParse().parse_args()

        query_args = []
        if req_val['published'] != 0: query_args.append(Article.published == req_val['published'] - 1)
        if req_val['delete'] != 0: query_args.append(Article.is_delete == req_val['delete'] - 1)
        if req_val.get('category', None): query_args.append(Article.category_id == req_val['category'])
        if req_val['recom'] != 0: query_args.append(Article.recom == req_val['recom'] - 1)
        if req_val.get("word", None): query_args.append(or_(
            Article.title.like('%' + req_val['word'] + '%'),
            Article.content.like('%' + req_val['word'] + '%')
        ))
        article = Article.query.filter(*query_args).order_by(Article.create_time.desc()).paginate(req_val['page'], req_val['rows'])

        page_data = {"page": article.page, "rows": req_val['rows'], "total_page": article.pages}
        return {"code": 200, "data": marshal(article.items, article_list_field), "page_data": page_data}






