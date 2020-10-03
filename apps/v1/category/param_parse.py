from common.libs.parse import BaseParse
from common.libs import inputs
from common.models.models import MODULES, Category, Upload
from flask import abort


class AddCategoryParse(BaseParse):
    def add_arguments(self):
        self.parse.add_arguments("title", type=inputs.str_range(1, 128), required=True)
        self.parse.add_arguments("sort", type=inputs.positive, default=20)
        self.parse.add_arguments("module", type=inputs.str_range(1, 32), choices=MODULES)
        self.parse.add_arguments("show", type=int, choices=(0, 1))
        self.parse.add_arguments("upper_id", type=inputs.data_exist(Category))
        self.parse.add_arguments("image_id", type=inputs.data_exist(Upload, re_obj=True))
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
    pass

