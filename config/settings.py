import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'fgz_home_system')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 200
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    STATIC_FOLDER = UPLOAD_FOLDER
    ALLOWED_IMAGE = ['png', 'jpg', 'jpeg']
    ALLOWED_FILE = ['xlsx']
    ALLOWED_EXTENSIONS = ALLOWED_IMAGE + ALLOWED_FILE
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB

    # 无需登陆接口
    WHITE_URL = ["/api/user/login", "/api/admin/login", "/api/user/sign_up"]

    # 管理员接口
    ADMIN_URL = []

    # redis数据库
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DB = 8  # 数据库名


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:qazplm123@127.0.0.1:3306/ljt_blog?charset=utf8'
    WEB_HOST_NAME = 'http://127.0.0.1:5000/'


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:qazplm123@172.24.34.25:3306/ljt_blog?charset=utf8'
    WEB_HOST_NAME = 'http://longjiangtao.top/'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:qazplm123@172.24.34.25:3306/ljt_blog?charset=utf8'
    WEB_HOST_NAME = 'http://longjiangtao.top/'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}