"""empty message

Revision ID: a1d2788d7d53
Revises: e283280e12be
Create Date: 2021-12-04 16:11:05.998074

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a1d2788d7d53'
down_revision = 'e283280e12be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('user_name', sa.String(length=250), nullable=False),
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('character_name', sa.String(length=250), nullable=True),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.Column('planet_name', sa.String(length=250), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['character.id'], ),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('favorite__character')
    op.drop_table('favorite__planet')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite__planet',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_name', mysql.VARCHAR(length=250), nullable=False),
    sa.Column('planet_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('planet_name', mysql.VARCHAR(length=250), nullable=False),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], name='favorite__planet_ibfk_1'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='favorite__planet_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('favorite__character',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_name', mysql.VARCHAR(length=250), nullable=False),
    sa.Column('character_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('character_name', mysql.VARCHAR(length=250), nullable=False),
    sa.ForeignKeyConstraint(['character_id'], ['character.id'], name='favorite__character_ibfk_1'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='favorite__character_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('favorite')
    # ### end Alembic commands ###
