"""return

Revision ID: ae5e8398ade7
Revises: a7067a783d0f
Create Date: 2020-10-28 17:38:28.723637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae5e8398ade7'
down_revision = 'a7067a783d0f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('patrons')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('patrons',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('is_patron', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='patrons_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='patrons_pkey'),
    sa.UniqueConstraint('email', name='patrons_email_key')
    )
    # ### end Alembic commands ###
