from common.models.base import Base, db
from common.libs.utility import *
from common.libs.redis import Redis


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

    @classmethod
    def check_token(cls, token):
        token_data = decrypt(token)
        if not token_data: return {"status": "failure", "msg": "token有误"}
        redis_obj = Redis()
        current_token = redis_obj.read('user_token_%s' % token_data['id'])
        if current_token != token: return {"status": "failure", "msg": "您的账号已在别处登录"}
        user = User.query.filter(User.id == token_data['id'], User.is_delete == 0).first()
        return {"status": "success", "user": user}