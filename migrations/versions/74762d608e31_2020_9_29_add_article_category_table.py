"""2020_9_29 add article category table

Revision ID: 74762d608e31
Revises: 69d7bf9cd0a3
Create Date: 2020-09-29 11:24:47.638645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74762d608e31'
down_revision = '69d7bf9cd0a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('create_time', sa.DateTime(), nullable=False, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), nullable=False, comment='更新时间'),
    sa.Column('is_delete', sa.SmallInteger(), nullable=True, comment='删除标识'),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False, comment='栏目名'),
    sa.Column('sort', sa.SmallInteger(), nullable=True, comment='排序值'),
    sa.Column('level', sa.SmallInteger(), nullable=True, comment='栏目等级'),
    sa.Column('module', sa.String(length=32), nullable=True, comment='所属模块'),
    sa.Column('upper_id', sa.Integer(), nullable=True),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['image_id'], ['upload.id'], ),
    sa.ForeignKeyConstraint(['upper_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('artice',
    sa.Column('create_time', sa.DateTime(), nullable=False, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), nullable=False, comment='更新时间'),
    sa.Column('is_delete', sa.SmallInteger(), nullable=True, comment='删除标识'),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False, comment='文章标题'),
    sa.Column('content', sa.Text(), nullable=True, comment='文章内容'),
    sa.Column('comment', sa.Integer(), nullable=True, comment='评论人数'),
    sa.Column('agree', sa.Integer(), nullable=True, comment='点赞人数'),
    sa.Column('click', sa.Integer(), nullable=True, comment='浏览次数'),
    sa.Column('recom', sa.SmallInteger(), nullable=True, comment='是否推荐，0否1是'),
    sa.Column('published', sa.SmallInteger(), nullable=True, comment='是否发布0否1是'),
    sa.Column('cover_id', sa.Integer(), nullable=True, comment='封面'),
    sa.Column('category_id', sa.Integer(), nullable=True, comment='栏目'),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['cover_id'], ['upload.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('artice')
    op.drop_table('category')
    # ### end Alembic commands ###