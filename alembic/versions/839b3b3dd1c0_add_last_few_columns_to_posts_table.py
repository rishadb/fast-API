"""add last few columns to posts table

Revision ID: 839b3b3dd1c0
Revises: 3213761e04c6
Create Date: 2022-06-29 17:26:13.160020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '839b3b3dd1c0'
down_revision = '3213761e04c6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
