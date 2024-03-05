"""Siswa: Add picture (BLOB)

Revision ID: 3d7dc9f3bb86
Revises: d6dd3ddca4b9
Create Date: 2024-03-05 09:42:43.667229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d7dc9f3bb86'
down_revision = 'd6dd3ddca4b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('siswa', schema=None) as batch_op:
        batch_op.add_column(sa.Column('picture', sa.BLOB(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('siswa', schema=None) as batch_op:
        batch_op.drop_column('picture')

    # ### end Alembic commands ###