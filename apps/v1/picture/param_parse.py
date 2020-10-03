from common.libs import inputs
from common.libs.parse import BaseParse


class PictureAlbumListParse(BaseParse):
    def add_arguments(self):

        self.parse.add_argument("page", type=inputs.positive, default=1)
        self.parse.add_argument("rows", type=inputs.positive, default=10)
        self.parse.add_argument("word", type=str)


class PictureInfoParse(PictureAlbumListParse):
    pass


class AddPictureAlbumParse(BaseParse):
    def add_arguments(self):
        self.parse.add_argument("title", type=inputs.str_range(1, 128), required=True)
        self.parse.add_argument("description", type=str)
        self.parse.add_argument('show', type=int, choices=(0, 1))


class UpdatePictureAlbumParse(AddPictureAlbumParse):
    pass



