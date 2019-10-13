"""empty message

Revision ID: e9f9b9178e86
Revises: 0ab4a25dfb6e
Create Date: 2019-10-05 15:11:16.852416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9f9b9178e86'
down_revision = '0ab4a25dfb6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_role', sa.Column('description', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_role', 'description')
    # ### end Alembic commands ###