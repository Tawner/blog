from common.libs.parse import BaseParse
from common.libs import inputs
from common.models.models import Category
from flask import abort


class ArticleListParse(BaseParse):
    def add_arguments(self):
        self.parse.add_argument("category", type=inputs.data_exist(Category, re_obj=True), required=True)
        self.parse.add_argument("word", type=str)
        self.parse.add_argument("page", type=int, default=1)
        self.parse.add_argument("rows", type=int, default=10)

    def other_parse(self):
        category = self.params.pop("category")
        if category.module != "article":
            return abort(400, message={"category": "请选择正确的文章栏目"})
        self.params['category'] = category.id

