"""empty message

Revision ID: a4fc2b3432e4
Revises: 
Create Date: 2024-05-29 12:57:27.154317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4fc2b3432e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('entry',
    sa.Column('entry_id', sa.Integer(), nullable=False),
    sa.Column('show_id', sa.Integer(), nullable=False),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('is_watched', sa.Boolean(), nullable=False),
    sa.Column('date_added', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['show_id'], ['show.show_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('entry_id')
    )
    op.drop_table('watch_list')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('watch_list',
    sa.Column('entry_id', sa.INTEGER(), nullable=False),
    sa.Column('show_id', sa.INTEGER(), nullable=False),
    sa.Column('notes', sa.TEXT(), nullable=True),
    sa.Column('is_watched', sa.BOOLEAN(), nullable=False),
    sa.Column('date_added', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['show_id'], ['show.show_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('entry_id')
    )
    op.drop_table('entry')
    # ### end Alembic commands ###