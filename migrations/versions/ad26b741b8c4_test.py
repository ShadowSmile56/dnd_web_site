"""test

Revision ID: ad26b741b8c4
Revises: 18b1955f4dd0
Create Date: 2021-12-23 12:36:54.811649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad26b741b8c4'
down_revision = '18b1955f4dd0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('company', 'dungeonmaster',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('company', 'dungeonmaster',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
