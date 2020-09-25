from .base import Base, db


class Article(Base):
    __tablename__ = "artice"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False, comment="文章标题")
    content = db.Column(db.Text, comment="文章内容")
    comment = db.Column(db.Integer, comment="评论人数", default=0)
    agree = db.Column(db.Integer, comment="点赞人数", default=0)
    click = db.Column(db.Integer, comment="浏览次数", default=0)
    recom = db.Column(db.SmallInteger, default=0, comment="是否推荐，0否1是")
    published = db.Column(db.SmallInteger, default=1, comment="是否发布0否1是")


    # 外键关联
    cover_id = db.Column(db.Integer, db.ForeignKey("upload.id"), comment="封面")
    cover = db.relationship("Upload", foreign_keys=[cover_id])
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), comment="栏目")
    category = db.relationship("Category", foreign_keys=[category_id])





