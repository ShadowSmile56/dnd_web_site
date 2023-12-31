"""customers table

Revision ID: a2dce4081639
Revises: 
Create Date: 2021-12-21 19:21:45.752779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2dce4081639'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book',
    sa.Column('namebook', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('namebook')
    )
    op.create_table('company',
    sa.Column('namecompany', sa.String(), nullable=False),
    sa.Column('discription', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('namecompany')
    )
    op.create_table('customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('login', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('surname', sa.String(), nullable=True),
    sa.Column('forename', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login')
    )
    op.create_table('place',
    sa.Column('numberroom', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('numberroom')
    )
    op.create_table('roles',
    sa.Column('namerole', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('namerole')
    )
    op.create_table('skill',
    sa.Column('skill', sa.String(), nullable=False),
    sa.Column('discription', sa.String(), nullable=False),
    sa.Column('skilllevel', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('skill')
    )
    op.create_table('bookcompany',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('namebook', sa.String(), nullable=False),
    sa.Column('namecompany', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['namebook'], ['book.namebook'], ),
    sa.ForeignKeyConstraint(['namecompany'], ['company.namecompany'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bookcompany_namebook'), 'bookcompany', ['namebook'], unique=False)
    op.create_index(op.f('ix_bookcompany_namecompany'), 'bookcompany', ['namecompany'], unique=False)
    op.create_table('customerscompany',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('namecompany', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['login'], ['customers.login'], ),
    sa.ForeignKeyConstraint(['namecompany'], ['company.namecompany'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customerscompany_login'), 'customerscompany', ['login'], unique=True)
    op.create_index(op.f('ix_customerscompany_namecompany'), 'customerscompany', ['namecompany'], unique=False)
    op.create_table('hero',
    sa.Column('namehero', sa.String(), nullable=False),
    sa.Column('strength', sa.Integer(), nullable=False),
    sa.Column('dexterity', sa.Integer(), nullable=False),
    sa.Column('physique', sa.Integer(), nullable=False),
    sa.Column('intelligence', sa.Integer(), nullable=False),
    sa.Column('wisdom', sa.Integer(), nullable=False),
    sa.Column('charisma', sa.Integer(), nullable=False),
    sa.Column('classhero', sa.String(), nullable=False),
    sa.Column('forename', sa.String(), nullable=True),
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('herolevel', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['login'], ['customers.login'], ),
    sa.PrimaryKeyConstraint('namehero','login')
    )
    op.create_index(op.f('ix_hero_login'), 'hero', ['login'], unique=True)
    op.create_table('news',
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('datet', sa.Date(), nullable=False),
    sa.Column('discription', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['login'], ['customers.login'], ),
    sa.PrimaryKeyConstraint('title')
    )
    op.create_index(op.f('ix_news_login'), 'news', ['login'], unique=True)
    op.create_table('play',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('numberroom', sa.Integer(), nullable=False),
    sa.Column('datet', sa.Date(), nullable=False),
    sa.Column('namecompany', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['namecompany'], ['company.namecompany'], ),
    sa.ForeignKeyConstraint(['numberroom'], ['place.numberroom'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_play_namecompany'), 'play', ['namecompany'], unique=False)
    op.create_index(op.f('ix_play_numberroom'), 'play', ['numberroom'], unique=False)
    op.create_table('roleuser',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('namerole', sa.String(), nullable=False),
    sa.Column('login', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['login'], ['customers.login'], ),
    sa.ForeignKeyConstraint(['namerole'], ['roles.namerole'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roleuser_login'), 'roleuser', ['login'], unique=True)
    op.create_index(op.f('ix_roleuser_namerole'), 'roleuser', ['namerole'], unique=False)
    op.create_table('artefact',
    sa.Column('artefactname', sa.String(), nullable=False),
    sa.Column('discription', sa.String(), nullable=False),
    sa.Column('namehero', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['namehero'], ['hero.namehero'], ),
    sa.PrimaryKeyConstraint('artefactname')
    )
    op.create_index(op.f('ix_artefact_namehero'), 'artefact', ['namehero'], unique=False)
    op.create_table('customersplay',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('idgame', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['idgame'], ['play.id'], ),
    sa.ForeignKeyConstraint(['login'], ['customers.login'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customersplay_idgame'), 'customersplay', ['idgame'], unique=False)
    op.create_index(op.f('ix_customersplay_login'), 'customersplay', ['login'], unique=True)
    op.create_table('skillhero',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('namehero', sa.String(), nullable=False),
    sa.Column('skill', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['namehero'], ['hero.namehero'], ),
    sa.ForeignKeyConstraint(['skill'], ['skill.skill'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_skillhero_namehero'), 'skillhero', ['namehero'], unique=True)
    op.create_index(op.f('ix_skillhero_skill'), 'skillhero', ['skill'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_skillhero_skill'), table_name='skillhero')
    op.drop_index(op.f('ix_skillhero_namehero'), table_name='skillhero')
    op.drop_table('skillhero')
    op.drop_index(op.f('ix_customersplay_login'), table_name='customersplay')
    op.drop_index(op.f('ix_customersplay_idgame'), table_name='customersplay')
    op.drop_table('customersplay')
    op.drop_index(op.f('ix_artefact_namehero'), table_name='artefact')
    op.drop_table('artefact')
    op.drop_index(op.f('ix_roleuser_namerole'), table_name='roleuser')
    op.drop_index(op.f('ix_roleuser_login'), table_name='roleuser')
    op.drop_table('roleuser')
    op.drop_index(op.f('ix_play_numberroom'), table_name='play')
    op.drop_index(op.f('ix_play_namecompany'), table_name='play')
    op.drop_table('play')
    op.drop_index(op.f('ix_news_login'), table_name='news')
    op.drop_table('news')
    op.drop_index(op.f('ix_hero_login'), table_name='hero')
    op.drop_table('hero')
    op.drop_index(op.f('ix_customerscompany_namecompany'), table_name='customerscompany')
    op.drop_index(op.f('ix_customerscompany_login'), table_name='customerscompany')
    op.drop_table('customerscompany')
    op.drop_index(op.f('ix_bookcompany_namecompany'), table_name='bookcompany')
    op.drop_index(op.f('ix_bookcompany_namebook'), table_name='bookcompany')
    op.drop_table('bookcompany')
    op.drop_table('skill')
    op.drop_table('roles')
    op.drop_table('place')
    op.drop_table('customers')
    op.drop_table('company')
    op.drop_table('book')
    # ### end Alembic commands ###
