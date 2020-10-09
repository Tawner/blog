from common.libs.parse import BaseParse
from common.libs import inputs
from common.models.models import MODULES, Category, Upload
from flask import abort


class AddCategoryParse(BaseParse):
    def add_arguments(self):
        self.parse.add_argument("title", type=inputs.str_range(1, 128), required=True)
        self.parse.add_argument("sort", type=inputs.positive, default=20)
        self.parse.add_argument("module", type=inputs.str_range(1, 32), choices=MODULES, required=True)
        self.parse.add_argument("show", type=int, choices=(0, 1))
        self.parse.add_argument("upper_id", type=inputs.data_exist(Category))
        self.parse.add_argument("image_id", type=inputs.data_exist(Upload, re_obj=True))
        # level = db.Column(db.SmallInteger, comment="栏目等级")

    def other_parse(self):
        # 图片校验
        if "image_id" in self.params.keys():
            image = self.params['image_id']
            if image.file_type != 0:
                return abort(400, message={"image_id": "图片不存在"})
            else:
                self.params['image_id'] = image.id
        # 栏目等级
        self.params['level'] = 2 if self.params.get("upper_id", None) else 1


class UpdateCategoryParse(BaseParse):
    def add_arguments(self):
        self.parse.add_argument("title", type=inputs.str_range(1, 128), required=True)
        self.parse.add_argument("sort", type=inputs.positive, default=20)
        self.parse.add_argument("show", type=int, choices=(0, 1))
        self.parse.add_argument("upper_id", type=inputs.data_exist(Category, re_obj=True))
        self.parse.add_argument("image_id", type=inputs.data_exist(Upload, re_obj=True))

    def other_parse(self):
        # 图片校验
        if "image_id" in self.params.keys():
            image = self.params['image_id']
            if image.file_type != 0:
                return abort(400, message={"image_id": "图片不存在"})
            else:
                self.params['image_id'] = image.id
        # 栏目校验
        if "upper_id" in self.params.keys():
            upper = self.params.pop("upper_id")
            # 栏目等级
            if upper.level != 1: return abort(400, message={"upper_id": "只允许二级栏目"})
            r = {"level": 2, "upper_id": upper.id}
        else:
            r = {"level": 1, "upper_id": None}
        self.params.update(r)


class CategoryListAdminParse(BaseParse):
    def add_arguments(self):
        self.parse.add_argument("module", type=str, choices=MODULES)