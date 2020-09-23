from common.models import *
from flask import Flask
from flask_cors import CORS
from config.settings import config
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


def register_blueprints(app):
    """蓝图注册"""
    from apps.user.views import user_bp
    from apps.upload.views import upload_bp
    from apps.admin.views import admin_bp
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(upload_bp, url_prefix='/api/upload')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')


def register_plugin(app):
    """插件注册"""
    from common.models.base import db
    from flask_migrate import Migrate
    db.init_app(app)
    manager = Manager(app)
    migrate = Migrate(app, db)
    manager.add_command('db', MigrateCommand)
    return manager


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 跨域
    CORS(app)
    # 注册蓝图
    register_blueprints(app)
    # 注册插件
    manager = register_plugin(app)
    return app, manager



