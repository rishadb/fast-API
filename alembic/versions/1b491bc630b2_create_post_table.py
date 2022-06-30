"""create post table

Revision ID: 1b491bc630b2
Revises: 
Create Date: 2022-06-29 16:10:49.158329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b491bc630b2' #revision id
down_revision = None
branch_labels = None
depends_on = None

# both funcs need to be updated; this will create table; run alembic upgrade/downgrade 1b491bc630b2 in cmd to upgrade/downgrade

def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
