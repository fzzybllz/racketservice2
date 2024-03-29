"""adding strings

Revision ID: 09c930774cd3
Revises: 
Create Date: 2022-08-13 10:49:18.268703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09c930774cd3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('strings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('manufacturer', sa.String(length=20), nullable=False),
    sa.Column('model', sa.String(length=50), nullable=False),
    sa.Column('gauge', sa.String(length=10), nullable=False),
    sa.Column('length', sa.String(length=3), nullable=True),
    sa.Column('color', sa.String(length=10), nullable=True),
    sa.Column('structure', sa.String(length=20), nullable=True),
    sa.Column('price', sa.String(length=10), nullable=True),
    sa.Column('consumption', sa.String(length=5), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('strings')
    # ### end Alembic commands ###
