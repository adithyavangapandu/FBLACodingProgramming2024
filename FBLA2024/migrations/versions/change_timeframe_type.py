"""empty message

Revision ID: 5d052dead829
Revises: 3821f6673dbb
Create Date: 2024-03-12 20:37:25.551323

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d052dead829'
down_revision = '3821f6673dbb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('partner', schema=None) as batch_op:
        batch_op.alter_column('timeframe',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('partner', schema=None) as batch_op:
        batch_op.alter_column('timeframe',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=True)

    # ### end Alembic commands ###
