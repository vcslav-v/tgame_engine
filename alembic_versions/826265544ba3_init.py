"""Init

Revision ID: 826265544ba3
Revises: 
Create Date: 2020-10-20 18:20:58.002222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '826265544ba3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('telegram_id', sa.Integer(), nullable=True),
    sa.Column('story_branch', sa.String(), nullable=True),
    sa.Column('point', sa.Integer(), nullable=True),
    sa.Column('last_activity', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
