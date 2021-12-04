"""empty message

Revision ID: 5ac6c2867896
Revises: 3a77af9deea1
Create Date: 2021-12-04 15:26:34.067313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ac6c2867896'
down_revision = '3a77af9deea1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('favorite', sa.Column('user_name', sa.String(length=250), nullable=False))
    op.add_column('favorite', sa.Column('character_name', sa.String(length=250), nullable=False))
    op.add_column('favorite', sa.Column('planet_name', sa.String(length=250), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('favorite', 'planet_name')
    op.drop_column('favorite', 'character_name')
    op.drop_column('favorite', 'user_name')
    # ### end Alembic commands ###
