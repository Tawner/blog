from common.libs.parse import *
from common.models.upload import Upload


class AddUserParse(BaseParse):
    def add_arguments(self):
        self.parse.add_argument('username', type=inputs.str_range(6, 16), required=True)
        self.parse.add_argument('password', type=inputs.str_range(6, 32), required=True)
        self.parse.add_argument('password_2', type=inputs.str_range(6, 32), required=True)
        self.parse.add_argument('nickname', type=inputs.str_range(3, 32), default='user')
        self.parse.add_argument('email', type=inputs.str_range(3, 128))
        self.parse.add_argument('phone', type=inputs.str_range(11, 11))
        self.parse.add_argument('image_id', type=inputs.data_exist(Upload, re_obj=True))

    def other_parse(self):
        # 密码一致性
        if self.params['password'] != self.params.pop('password_2'):
            return abort(400, message={"password": "两次密码不一致"})
        # 图片存在判断
        image = self.params.get("image_id", None)
        if image:
            if image.file_type != 0: return abort(400, message={"image_id": "图片不存在"})
            else: self.params['image_id'] = image.id


class UpdateUserParse(BaseParse):
    def add_arguments(self):
        self.parse.add_argument('password', type=inputs.str_range(6, 32))
        self.parse.add_argument('password_2', type=inputs.str_range(6, 32))
        self.parse.add_argument('nickname', type=inputs.str_range(3, 32))
        self.parse.add_argument('email', type=inputs.str_range(3, 128))
        self.parse.add_argument('phone', type=inputs.str_range(11, 11))
        self.parse.add_argument('image_id', type=inputs.data_exist(Upload, re_obj=True))

    def other_parse(self):
        # 密码一致性
        if self.params.get("password", '') != self.params.get("password_2", ""):
            return abort(400, message={"password": "两次密码不一致"})
        if "password_2" in self.params.keys(): self.params.pop("password_2")
        # 图片存在
        image = self.params.get("image_id", None)
        if image:
            if image.file_type != 0: return abort(400, message={"image_id": "图片不存在"})
            else: self.params['image_id'] = image.id


class UserLoginParse(BaseParse):
    def add_arguments(self):
        self.parse.add_argument('username', type=inputs.str_range(6, 16), required=True)
        self.parse.add_argument('password', type=inputs.str_range(6, 32), required=True)



