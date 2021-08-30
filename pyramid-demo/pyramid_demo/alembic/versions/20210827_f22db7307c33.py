"""init

Revision ID: f22db7307c33
Revises: d21ec44b7c6b
Create Date: 2021-08-27 10:05:10.999639

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f22db7307c33'
down_revision = 'd21ec44b7c6b'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('category', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_products'))
    )
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    # ### end Alembic commands ###
