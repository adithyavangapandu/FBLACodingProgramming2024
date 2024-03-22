"""empty message

Revision ID: 48dbb9a7c8cf
Revises: 
Create Date: 2024-03-11 14:42:50.439473

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48dbb9a7c8cf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('partner', schema=None) as batch_op:
        batch_op.add_column(sa.Column('money', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('time', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('partner', schema=None) as batch_op:
        batch_op.drop_column('time')
        batch_op.drop_column('money')

    # ### end Alembic commands ###