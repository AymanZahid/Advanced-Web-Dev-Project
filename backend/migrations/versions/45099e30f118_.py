"""empty message

Revision ID: 45099e30f118
Revises: 
Create Date: 2024-10-27 17:55:03.298568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45099e30f118'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('salt', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('move',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('power', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('accuracy', sa.Integer(), nullable=True),
    sa.Column('pp', sa.Integer(), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['type.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('pokemon',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.Column('hp', sa.Integer(), nullable=False),
    sa.Column('attack', sa.Integer(), nullable=False),
    sa.Column('defense', sa.Integer(), nullable=False),
    sa.Column('sp_attack', sa.Integer(), nullable=False),
    sa.Column('sp_defense', sa.Integer(), nullable=False),
    sa.Column('speed', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('pokemon_move',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('pokemon_id', sa.Integer(), nullable=False),
    sa.Column('move_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['move_id'], ['move.id'], ),
    sa.ForeignKeyConstraint(['pokemon_id'], ['pokemon.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pokemon_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('pokemon_id', sa.Integer(), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pokemon_id'], ['pokemon.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pokemon_type')
    op.drop_table('pokemon_move')
    op.drop_table('pokemon')
    op.drop_table('move')
    op.drop_table('type')
    op.drop_table('account')
    # ### end Alembic commands ###
