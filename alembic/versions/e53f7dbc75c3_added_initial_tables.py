"""Added initial tables

Revision ID: e53f7dbc75c3
Revises: 
Create Date: 2023-03-20 00:41:42.766356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e53f7dbc75c3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('game_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('game_id')
    )
    op.create_table('player',
    sa.Column('vk_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=45), nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=45), nullable=False),
    sa.PrimaryKeyConstraint('vk_id')
    )
    op.create_table('user',
    sa.Column('vk_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=45), nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=45), nullable=False),
    sa.PrimaryKeyConstraint('vk_id')
    )
    op.create_table('player_game_score',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('vk_id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['game.game_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['vk_id'], ['player.vk_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('player_game_score')
    op.drop_table('user')
    op.drop_table('player')
    op.drop_table('game')
    # ### end Alembic commands ###
