"""empty message

Revision ID: e2736e27c129
Revises: 17b4ca2fcbc7
Create Date: 2020-10-27 18:42:19.126642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2736e27c129'
down_revision = '17b4ca2fcbc7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('queue_message', sa.Column('is_story', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('queue_message', 'is_story')
    # ### end Alembic commands ###
