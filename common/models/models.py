from .base import Base, db
from common.libs.utility import *
from flask import current_app
from common.libs.redis import Redis
import os
MODULES = ("article", "picture")


class Upload(Base):
    __tablename__ = 'upload'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(252), comment='文件名')
    file_md5 = db.Column(db.String(128), comment='文件md5')
    file_type = db.Column(db.SmallInteger, default=0, comment='文件类型')  # 0 图片 1 文件
    file_size = db.Column(db.Integer, default=0, comment='文件大小')
    path = db.Column(db.String(256), comment='文件路径')

    @property
    def url(self):
        path = 'file/' if self.file_type else 'image/'
        url = current_app.config['WEB_HOST_NAME'] + 'api/uploads/' + path + self.filename
        return url

    @classmethod
    def save_file(cls, file):
        if not file: return {'status': "failure", "msg": "没有上传文件"}

        filename, file_type = os.path.splitext(file.filename)
        if file_type[1:] in current_app.config['ALLOWED_IMAGE']: upload_type = 0
        elif file_type[1:] in current_app.config['ALLOWED_file']: upload_type = 1
        else: return {"status": "failure", "msg": "不允许上传的文件类型"}

        md5_code = md5(file.read())
        upload_file = Upload.query.filter(Upload.file_md5 == md5_code).first()
        if upload_file:
            return {"status": "success", "url": upload_file.url, 'id': upload_file.id}
        else:
            r_path = current_app.config['UPLOAD_FOLDER'] + 'file/' if upload_file else 'image/' + md5_code + file_type,
            inset_data = {
                "filename": md5_code + file_type,
                "file_md5": md5_code,
                "file_type": upload_type,
                "file_size": file.content_length,
                "path": r_path
            }
            upload_file = Upload(**inset_data)
            file.seek(0)
            file.save(r_path)
            db.session.add(upload_file)
            db.session.commit()
            return {"status": "success", "url": upload_file.url, 'id': upload_file.id}


class User(Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), nullable=False, comment='用户名')
    password = db.Column(db.String(32), nullable=False, comment='密码')
    encryption = db.Column(db.String(6), nullable=False, comment='密文')
    nickname = db.Column(db.String(32), comment='昵称')
    email = db.Column(db.String(128), comment='邮箱')
    phone = db.Column(db.String(11), comment='手机号码')
    superuser = db.Column(db.SmallInteger, comment="后台用户,0否1是")

    # 外键、关联
    image_id = db.Column(db.Integer, db.ForeignKey('upload.id'))
    headimg = db.relationship("Upload", foreign_keys=[image_id])

    @staticmethod
    def check_password(username, password, superuser=False):
        query_args = [User.username == username, User.is_delete == 0]
        if superuser: query_args.append(User.superuser == 1)
        else: query_args.append((User.superuser == 0))
        user = User.query.filter(*query_args).first()
        if not user: return {"status": "failure", "msg": "用户名不存在"}
        if md5(md5(password) + user.encryption) == user.password:
            return {"status": "success", "user": user}
        else:
            return {"status": "failure", "msg": "用户名或者密码错误"}

    @property
    def image(self):
        return self.headimg.url

    @classmethod
    def add(cls, username, password, nickname=None, email=None, phone=None, image_id=None, superuser=0):
        exist = User.query.filter(User.username == username, User.superuser == superuser).first()
        if exist: return {"status": "failure", "msg": "用户名已存在"}
        encryption = random_str(6)
        user = User(
            username=username,
            password=md5(md5(password) + encryption),
            encryption=encryption,
            nickname=nickname,
            email=email,
            phone=phone,
            image_id=image_id,
            superuser=superuser
        )
        db.session.add(user)
        db.session.commit()
        return {"status": "success", "user": user}

    def update(self, password=None, nickname=None, email=None, phone=None, image_id=None):
        if password: self.password = md5(md5(password) + self.encryption)
        if nickname: self.nickname = nickname
        if email: self.email = email
        if phone: self.phone = phone
        if image_id: self.image_id = image_id
        db.session.commit()
        return {"status": "success", "user": self}

    def create_token(self):
        token = encrypt({"id": self.id})
        redis_obj = Redis()
        redis_obj.write('user_token_%s' % self.id, token)
        return token

    @property
    def is_super(self):
        return True if self.superuser == 1 else False

    @classmethod
    def check_token(cls, token):
        token_data = decrypt(token)
        if not token_data: return {"status": "failure", "msg": "token有误"}
        redis_obj = Redis()
        current_token = redis_obj.read('user_token_%s' % token_data['id'])
        if current_token != token: return {"status": "failure", "msg": "您的账号已在别处登录"}
        user = User.query.filter(User.id == token_data['id'], User.is_delete == 0).first()
        return {"status": "success", "user": user}


class Article(Base):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False, comment="文章标题")
    content = db.Column(db.Text, comment="文章内容")
    comment = db.Column(db.Integer, comment="评论人数", default=0)
    agree = db.Column(db.Integer, comment="点赞人数", default=0)
    click = db.Column(db.Integer, comment="浏览次数", default=0)
    recom = db.Column(db.SmallInteger, default=0, comment="是否推荐，0否1是")
    published = db.Column(db.SmallInteger, default=1, comment="是否发布0否1是")
    publish_date = db.Column(db.DateTime, nullable=False, default=db.func.now(), comment='发布时间')

    # 外键关联
    cover_id = db.Column(db.Integer, db.ForeignKey("upload.id"), comment="封面")
    cover = db.relationship("Upload", foreign_keys=[cover_id])
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), comment="栏目")
    category = db.relationship("Category", foreign_keys=[category_id])

    @property
    def cover_image(self):
        return self.cover.url


class Category(Base):
    MODULE_TYPE = {
        "article": Article
    }
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False, comment="栏目名")
    sort = db.Column(db.SmallInteger, default=20, comment="排序值")
    level = db.Column(db.SmallInteger, comment="栏目等级")
    module = db.Column(db.String(32), comment="所属模块")
    show = db.Column(db.SmallInteger, default=1, comment="前台是否展示,0否1是")

    # 外键、关联
    upper_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    image_id = db.Column(db.Integer, db.ForeignKey("upload.id"))
    image = db.relationship("Upload", foreign_keys=[image_id])

    @property
    def sub_section(self):
        """获取显示的子栏目"""
        category = Category.query.filter(Category.upper_id == self.id, Category.is_delete == 0).all()
        return category

    @property
    def lower(self):
        category = Category.query.filter(
            Category.upper_id == self.id,
            Category.is_delete == 0,
            Category.show == 1
        ).all()
        return category

    @classmethod
    def empty(self):
        """是否为空栏目"""
        sub = Category.query.filter(
            Category.upper_id == self.id,
            Category.is_delete == 0
        ).all()
        model = self.MODULE_TYPE.get(self.module)
        content = model.query.filter(model.category_id == self.id, model.is_delete == 0).all()
        return False if sub or content else True

    @property
    def upper(self):
        category = Category.query.get(self.upper_id)
        return category if category else None

    @property
    def category_structure(self):
        res = [self.upper, self] if self.upper_id else [self]
        return res


class PictureAlbum(Base):
    __tablename__ = "picture_album"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False, comment="图集名")
    description = db.Column(db.Text, comment="图集描述")
    show = db.Column(db.SmallInteger, default=1, comment="是否展示0否1是")

    # 外键关联
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), comment="栏目")
    category = db.relationship("Category", foreign_keys=[category_id])


class Picture(Base):
    __tablename__ = "picture"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), comment="标题")
    description = db.Column(db.Text, comment="描述")
    url = db.Column(db.String(255), comment="跳转地址")

    # 外键关联
    image_id = db.Column(db.Integer, db.ForeignKey("upload.id"))
    image = db.relationship("Upload", foreign_keys=[image_id])
    picture_album_id = db.Column(db.Integer, db.ForeignKey("picture_album.id"))
    picture_album = db.relationship("PictureAlbum", foreign_keys=[picture_album_id], backref="picture")

