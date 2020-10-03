from common.models.models import Picture, PictureAlbum
from flask_restful import Resource, marshal
from .param_parse import *
from sqlalchemy import or_
from .marshals import *


# 前台接口
class PictureAlbumListView(Resource):
    def get(self):
        req_val = PictureAlbumListParse().parse_args()

        query_args = [PictureAlbum.is_delete == 0, PictureAlbum.show == 1]
        if req_val.get("word", None):
            query_args.append(or_(
                PictureAlbum.title.like("%" + req_val['word'] + "%"),
                PictureAlbum.description.like("%" + req_val['word'] + "%")
            ))
        picture_album = PictureAlbum.qeury.filter(*query_args).paginate(req_val['page'], req_val['rows'])
        page_data = {"page": picture_album.page, "rows": req_val['rows'], "total_page": picture_album.pages}
        return {"code": 200, "data": marshal(picture_album.items, picture_album_filed), "page_data": page_data}


class PictureInfoView(Resource):
    def get(self, album_id):
        req_val = PictureInfoParse().parse_args()

        picture_album = PictureAlbum.query.filter(
            PictureAlbum.id == album_id,
            PictureAlbum.is_delete == 0,
            PictureAlbum.show == 1
        ).first_or_404()

        query_args = [Picture.is_delete == 0, Picture.picture_album_id == album_id]
        if req_val.get("word", None):
            query_args.append(or_(
                Picture.title.like("%" + req_val['word'] + "%"),
                Picture.description.like("%" + req_val['word'] + "%")
            ))
        picture = Picture.query.filter(*query_args).paginate(req_val['page'], req_val['rows'])
        page_data = {"page": picture.page, "rows": req_val['rows'], "total_page": picture.pages}
        return {"code": 200, "data": marshal(picture.items, picture_info_filed), "page_data": page_data}


# 后台接口
class AddPictureAlbumView(Resource):
    def post(self):
        AddPictureAlbumParse().parse_args()


class PictureAlbumInfoView(Resource):
    def get(self, album_id):
        pass

    def put(self, album_id):
        pass

    def delete(self, album_id):
        pass


class AddPictureView(Resource):
    def post(self, album_id):
        pass


class PictureInfoAdminView(Resource):
    def get(self, picture_id):
        pass

    def put(self, picture_id):
        pass

    def delete(self, picture_id):
        pass


