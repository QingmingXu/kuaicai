"""empty message

Revision ID: e3a4d4b50289
Revises: 60213bd295e8
Create Date: 2019-03-25 03:51:06.945820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3a4d4b50289'
down_revision = '60213bd295e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=1024), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('pay_way', sa.String(length=32), nullable=True),
    sa.Column('pay_status', sa.String(length=32), nullable=True),
    sa.Column('go_status', sa.String(length=32), nullable=True),
    sa.Column('order_status', sa.String(length=32), nullable=True),
    sa.Column('belong_to', sa.Integer(), nullable=True),
    sa.Column('order_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tb_order')
    # ### end Alembic commands ###
