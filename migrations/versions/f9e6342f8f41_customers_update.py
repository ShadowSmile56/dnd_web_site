"""customers update 

Revision ID: f9e6342f8f41
Revises: a2dce4081639
Create Date: 2021-12-21 22:23:52.670081

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9e6342f8f41'
down_revision = 'a2dce4081639'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hero', 'forename')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hero', sa.Column('forename', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###