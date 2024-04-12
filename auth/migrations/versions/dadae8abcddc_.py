"""empty message

Revision ID: dadae8abcddc
Revises: 5c40078f3de1
Create Date: 2024-03-31 00:44:20.129511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dadae8abcddc'
down_revision = '5c40078f3de1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('token_blocklist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('token_type', sa.String(length=10), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('token_blocklist', schema=None) as batch_op:
        batch_op.drop_column('token_type')

    # ### end Alembic commands ###