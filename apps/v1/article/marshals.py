from common.libs import fields


category_structure_fields = {
    "id": fields.Integer,
    "title": fields.String
}

category_info_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "level": fields.Integer,
    "module": fields.String,
    "image": fields.String(attribute="image.url")
}

article_info_field = {
    "id": fields.Integer,
    "title": fields.String,
    "content": fields.String,
    "comment": fields.Integer,
    "agree": fields.Integer,
    "click": fields.Integer,
    "cover_image": fields.String,
    "category": fields.Nested(category_info_fields),
    "category_structure": fields.Nested(category_structure_fields, attribute="category.category_structure"),
    "publish_date": fields.Datetime("%Y-%m-%d")
}

article_info_admin_field = {
    "recom": fields.Integer,
    "published": fields.Integer
}
article_info_admin_field.update(article_info_field)


article_list_field = {
    "id": fields.Integer,
    "title": fields.String,
    "comment": fields.Integer,
    "agree": fields.Integer,
    "click": fields.Integer,
    "cover_image": fields.String,
    "category": fields.Nested(category_info_fields),
}
