"""Add image_url to Product

Revision ID: 960f6faa17f6
Revises: 
Create Date: 2024-07-14 19:35:05.770437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '960f6faa17f6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_url', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_column('image_url')

    # ### end Alembic commands ###
