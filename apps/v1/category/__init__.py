from .views import *


def add_resource(api):
    api.add_resource(CategoryListView, '/category/list')
    api.add_resource(CategoryListAdminView, '/admin/category/list')
    api.add_resource(CategoryInfoAdminView, '/admin/category/info/<int:category_id>')
    api.add_resource(AddCategoryView, '/admin/category/info')