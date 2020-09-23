from .base import Base, db
from .article import Article
MODULE_TYPE = {"article": Article}


class Category(Base):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False, comment="栏目名")
    sort = db.Column(db.SmallInteger, default=20, comment="排序值")
    level = db.Column(db.SmallInteger, comment="栏目等级")
    module = db.Column(db.String(32), comment="所属模块")

    # 外键、关联
    upper_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    upper = db.relationship("Category", foreign_keys=[upper_id])
    image_id = db.Column(db.Integer, db.ForeignKey("upload.id"))
    image = db.relationship("Upload", foreign_keys=[image_id])

    def sub_section(self):
        """获取子栏目"""
        categorys = Category.query.filter(
            Category.upper_id == self.id,
            Category.is_delete == 0
        ).all()
        return categorys

    def empty(self):
        """是否为空栏目"""
        sub = Category.query.filter(
            Category.upper_id == self.id,
            Category.is_delete == 0
        ).all()
        model = MODULE_TYPE.get(self.module)
        content = model.query.filter(model.category_id == self.id, model.is_delete == 0).all()
        return False if sub or content else True


