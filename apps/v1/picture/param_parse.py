from common.libs import inputs
from common.libs.parse import BaseParse
from common.models.models import Category, Upload, PictureAlbum
from flask import abort


class PictureAlbumListParse(BaseParse):
    def add_arguments(self):
        self.parse.add_argument("category", type=inputs.data_exist(Category, re_obj=True))
        self.parse.add_argument("page", type=inputs.positive, default=1)
        self.parse.add_argument("rows", type=inputs.positive, default=10)
        self.parse.add_argument("word", type=str)

    def other_parse(self):
        if "category" in self.params.keys():
            category = self.params.pop("category")
            if category.module != "picture":
                return abort(400, message={"category": "请选择正确的图集栏目"})
            self.params['category'] = category.id


class PictureInfoParse(BaseParse):
    def add_arguments(self):
        self.parse.add_argument("page", type=inputs.positive, default=1)
        self.parse.add_argument("rows", type=inputs.positive, default=10)
        self.parse.add_argument("word", type=str)


class AddPictureAlbumParse(BaseParse):
    def add_arguments(self):
        self.parse.add_argument("title", type=inputs.str_range(1, 128), required=True)
        self.parse.add_argument("description", type=str)
        self.parse.add_argument('show', type=int, choices=(0, 1))
        self.parse.add_argument('category', type=inputs.data_exist(Category, re_obj=True), required=True)

    def other_parse(self):
        category = self.params.pop("category")
        if category.module != "picture":
            return abort(400, message={"category": "该图集栏目不存在"})
        self.params['category_id'] = category.id


class UpdatePictureAlbumParse(AddPictureAlbumParse):
    pass


class PictureAlbumListAdminParse(PictureAlbumListParse):
    pass


class AddPictureParse(BaseParse):
    def add_arguments(self):
        self.parse.add_argument("title", type=inputs.str_range(1, 128), required=True)
        self.parse.add_argument("description", type=str)
        self.parse.add_argument("url", type=inputs.str_range(1, 255))
        self.parse.add_argument("image_id", type=inputs.data_exist(Upload, re_obj=True), required=True)
        self.parse.add_argument("picture_album_id", type=inputs.data_exist(PictureAlbum), required=True)

    def other_parse(self):
        image = self.params.get("image_id", None)
        if image:
            if image.file_type != 0:
                return abort(400, message={"cover_id": "图片不存在"})
            else:
                self.params['image_id'] = image.id


class UpdatePictureParse(AddPictureParse):
    pass
