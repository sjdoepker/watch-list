"""empty message

Revision ID: 9bbca0912c82
Revises: 8f2785666a45
Create Date: 2024-06-11 21:14:45.083321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bbca0912c82'
down_revision = '8f2785666a45'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('pw',
               existing_type=sa.VARCHAR(),
               type_=sa.LargeBinary(),
               existing_nullable=False,
               postgresql_using="pw::bytea"
            )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('pw',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(),
               existing_nullable=False)

    # ### end Alembic commands ###