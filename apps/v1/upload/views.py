from common.models.upload import *
from flask_restful import Resource, Api
from flask import Blueprint
from flask import request
from common.libs.utility import *

upload_bp = Blueprint('upload', __name__)
upload_api = Api(upload_bp)


class UploadView(Resource):

    def post(self):
        file = request.files.get('file', None)
        if not file: return {'code': 201, "msg": "没有上传文件"}

        filename, file_type = os.path.splitext(file.filename)
        if file_type[1:] not in current_app.config['ALLOWED_EXTENSIONS']:
            return {"code": 203, "msg": "不允许上传的文件类型"}

        # 文件处理
        md5_code = md5(file.read())
        upload = Upload.query.filter(Upload.is_delete == 0, Upload.file_md5 == md5_code).first()

        # 文件保存
        if upload: return {"code": 200, "data": {"id": upload.id, "url": upload.url}}

        data = {
            "filename": md5(file.filename.encode("utf8")) + file_type,
            "file_md5": md5_code,
            "file_type": 0 if file_type[1:] in current_app.config['ALLOWED_IMAGE'] else 1,
            "file_size": file.content_length,
        }
        path = 'file/' if data['file_type'] else 'image/'
        data['path'] = os.path.join(current_app.config['UPLOAD_FOLDER'], path) + data['filename']
        upload = Upload(**data)

        file.seek(0)
        file.save(data['path'])
        db.session.add(upload)
        db.session.commit()
        return {"code": 200, "data": {"id": upload.id, "url": upload.url}}


upload_api.add_resource(UploadView, '')

