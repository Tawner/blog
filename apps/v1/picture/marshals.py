from common.libs import fields


picture_info_filed = {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
    "url": fields.String,
    "image": fields.String(attribute="image.url"),
    "picture_album_id": fields.Integer,
}

picture_info_admin_filed = {
    "create_time": fields.Datetime(dt_format="%Y-%m-%d %H:%M"),
    "update_time": fields.Datetime(dt_format="%Y-%m-%d %H:%M"),
}
picture_info_admin_filed.update(picture_info_filed)

picture_album_filed = {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
}

picture_album_admin_filed = {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
    "show": fields.Integer,
    "create_time": fields.Datetime(dt_format="%Y-%m-%d %H:%M"),
    "update_time": fields.Datetime(dt_format="%Y-%m-%d %H:%M"),
}