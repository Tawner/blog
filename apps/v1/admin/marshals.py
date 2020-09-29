from flask_restful import fields

admin_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "nickname": fields.String,
    "email": fields.String,
    "phone": fields.String,
    "image": fields.String
}


