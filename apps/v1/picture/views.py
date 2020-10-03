from common.models.models import Picture, PictureAlbum, db
from flask_restful import Resource, marshal
from .param_parse import *
from sqlalchemy import or_
from .marshals import *
from common.libs.login_require import *


# 前台接口
class PictureAlbumListView(Resource):
    def get(self):
        req_val = PictureAlbumListParse().parse_args()

        query_args = [PictureAlbum.is_delete == 0, PictureAlbum.show == 1]
        if req_val.get("category_id", None): query_args.append(PictureAlbum.category_id == req_val['category_id'])
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

        query_args = [Picture.is_delete == 0, Picture.picture_album_id == picture_album.id]
        if req_val.get("word", None):
            query_args.append(or_(
                Picture.title.like("%" + req_val['word'] + "%"),
                Picture.description.like("%" + req_val['word'] + "%")
            ))
        picture = Picture.query.filter(*query_args).paginate(req_val['page'], req_val['rows'])
        page_data = {"page": picture.page, "rows": req_val['rows'], "total_page": picture.pages}
        return {"code": 200, "data": marshal(picture.items, picture_info_filed), "page_data": page_data}


# 后台接口
class PictureAlbumListAdminView(Resource):
    @AdminLoginRequired
    def get(self):
        req_val = PictureAlbumListAdminParse().parse_args()

        query_args = [PictureAlbum.is_delete == 0]
        if req_val.get("category_id", None): query_args.append(PictureAlbum.category_id == req_val['category_id'])
        if req_val.get("word", None):
            query_args.append(or_(
                PictureAlbum.title.like("%" + req_val['word'] + "%"),
                PictureAlbum.description.like("%" + req_val['word'] + "%")
            ))
        picture_album = PictureAlbum.qeury.filter(*query_args).paginate(req_val['page'], req_val['rows'])
        page_data = {"page": picture_album.page, "rows": req_val['rows'], "total_page": picture_album.pages}
        return {"code": 200, "data": marshal(picture_album.items, picture_album_admin_filed), "page_data": page_data}


class AddPictureAlbumView(Resource):
    @AdminLoginRequired
    def post(self):
        req_val = AddPictureAlbumParse().parse_args()
        album = PictureAlbum(**req_val)
        db.session.add(album)
        db.session.commit()
        return {"code": 200, "msg": "添加成功"}


class PictureAlbumInfoView(Resource):
    @AdminLoginRequired
    def get(self, album_id):
        album = PictureAlbum.query.filter(PictureAlbum.is_delete == 0, PictureAlbum.id == album_id).first_or_404()
        return {"code": 200, "data": marshal(album, picture_album_admin_filed)}

    @AdminLoginRequired
    def put(self, album_id):
        req_val = UpdatePictureAlbumParse().parse_args()
        album = PictureAlbum.query.filter(PictureAlbum.is_delete == 0, PictureAlbum.id == album_id).first_or_404()
        album.set_attrs(req_val)
        db.session.commit()
        return {"code": 200, "msg": "修改成功"}

    @AdminLoginRequired
    def delete(self, album_id):
        album = PictureAlbum.query.filter(PictureAlbum.is_delete == 0, PictureAlbum.id == album_id).first_or_404()
        album.delete()
        return {"code": 200, "msg": "删除成功"}


class AddPictureView(Resource):
    @AdminLoginRequired
    def post(self):
        req_val = AddPictureParse().parse_args()
        picture = Picture(**req_val)
        db.session.add(picture)
        db.session.commit()
        return {"code": 200, "msg": "添加成功"}


class PictureInfoAdminView(Resource):
    @AdminLoginRequired
    def get(self, picture_id):
        picture = Picture.query.filter(Picture.id == picture_id, Picture.is_delete == 0).first_or_404()
        return {"code": 200, "data": marshal(picture, picture_info_admin_filed)}

    @AdminLoginRequired
    def put(self, picture_id):
        req_val = UpdatePictureParse().parse_args()
        picture = Picture.query.filter(Picture.id == picture_id, Picture.is_delete == 0).first_or_404()
        picture.set_attrs(req_val)
        db.session.commit()
        return {"code": 200, "msg": "修改成功"}

    @AdminLoginRequired
    def delete(self, picture_id):
        picture = Picture.query.filter(Picture.id == picture_id, Picture.is_delete == 0).first_or_404()
        picture.delete()
        return {"code": 200, "msg": "删除成功"}


