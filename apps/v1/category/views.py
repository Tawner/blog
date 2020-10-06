from flask_restful import Resource, marshal
from common.models.models import Category, db
from .marshals import *
from .param_parse import *
from common.libs.login_require import *


# 前台接口
class CategoryListView(Resource):
    """获取前台栏目列表结构"""
    def get(self):
        category = Category.query.filter(Category.is_delete == 0, Category.show == 1, Category.level == 1).all()
        return {"code": 200, "data": marshal(category, category_structure_field)}


# 后台接口
class CategoryListAdminView(Resource):
    """获取栏目列表"""
    @AdminLoginRequired
    def get(self):
        req_val = CategoryListAdminParse().parse_args()
        query_args = [Category.is_delete == 0, Category.level == 1]
        if req_val.get("module", None): query_args.append(Category.module == req_val['module'])
        category = Category.query.filter(*query_args).all()
        return {"code": 200, "data": marshal(category, category_structure_admin_field)}


class CategoryInfoAdminView(Resource):
    @AdminLoginRequired
    def get(self, category_id):
        category = Category.query.filter(Category.id == category_id, Category.is_delete == 0).first_or_404()
        return {"code": 200, "data": marshal(category, category_info_field)}

    @AdminLoginRequired
    def put(self, category_id):
        req_val = UpdateCategoryParse().parse_args()
        category = Category.query.filter(Category.id == category_id, Category.is_delete == 0).first_or_404()
        category.set_attrs(req_val)
        db.session.commit()
        return {"code": 200, "msg": "修改成功"}

    @AdminLoginRequired
    def delete(self, category_id):
        category = Category.query.filter(Category.id == category_id, Category.is_delete == 0).first_or_404()
        category.delete()
        return {"code": 200, "msg": "删除成功"}


class AddCategoryView(Resource):
    @AdminLoginRequired
    def post(self):
        req_val = AddCategoryParse().parse_args()
        category = Category(**req_val)
        db.session.add(category)
        db.session.commit()
        return {"code": 200, "msg": "添加成功"}

