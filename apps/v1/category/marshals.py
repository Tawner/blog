from common.libs import fields, inputs


category_info_field = {
    "id": fields.Integer,
    "title": fields.String,
    "sort": fields.Integer,
    "level": fields.Integer,
    "module": fields.String,
    "image": fields.String(attribute="image.url"),
    "category_structure": fields.Nested({"id": fields.Integer, "title": fields.String}),
}


category_structure_field = {
    "sub_section": fields.Nested(category_info_field),
}
category_structure_field.update(category_info_field)

category_structure_admin_field = {
    "lower": fields.Nested(category_info_field),
    "show": fields.Integer,
}
category_structure_admin_field.update(category_info_field)
