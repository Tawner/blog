from common.libs.parse import BaseParse
from common.libs import inputs
from common.models.models import Category
from flask import abort
from common.models.models import Upload, Category


class ArticleListParse(BaseParse):
    def add_arguments(self):
        self.parse.add_argument("category", type=inputs.data_exist(Category, re_obj=True))
        self.parse.add_argument("recom", type=int, choices=(0, 1, 2), default=0)  # 0所有，1不推荐，2推荐
        self.parse.add_argument("word", type=str)
        self.parse.add_argument("page", type=int, default=1)
        self.parse.add_argument("rows", type=int, default=10)

    def other_parse(self):
        if self.params.get("category", None):
            category = self.params.pop("category")
            if category.module != "article":
                return abort(400, message={"category": "请选择正确的文章栏目"})
            self.params['category_id'] = category.id


class ArticleListAdminParse(ArticleListParse):
    def add_arguments(self):
        super().add_arguments()
        self.parse.add_argument("delete", type=int, choices=(0, 1, 2), default=1)  # 0全部，2未删除，1已删除
        self.parse.add_argument('published', type=int, choices=(0, 1, 2), default=0)  # 0全部，2已发布，1未发布


class AddArticleParse(BaseParse):
    def add_arguments(self):
        self.parse.add_argument("title", type=inputs.str_range(1, 255), required=True)
        self.parse.add_argument("content", type=str)
        self.parse.add_argument("agree", type=inputs.positive, default=0)
        self.parse.add_argument("click", type=inputs.positive, default=0)
        self.parse.add_argument("published", type=int, choices=(0, 1), default=1)  # 0不发布，1发布
        self.parse.add_argument("recom", type=int, choices=(0, 1), default=1)  # 0不推荐，1推荐
        self.parse.add_argument("cover_id", type=inputs.data_exist(Upload, re_obj=True))
        self.parse.add_argument('category', type=inputs.data_exist(Category, re_obj=True), required=True)

    def other_parse(self):
        # 封面校验
        image = self.params.get("cover_id", None)
        if image:
            if image.file_type != 0:
                return abort(400, message={"cover_id": "图片不存在"})
            else:
                self.params['cover_id'] = image.id

        # 栏目校验
        category = self.params.pop("category")
        if category.module != "article":
            return abort(400, message={"category": "该文章栏目不存在"})
        self.params['category_id'] = category.id


class UpdateArticleParse(AddArticleParse):
    pass
