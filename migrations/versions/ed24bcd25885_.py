"""empty message

Revision ID: ed24bcd25885
Revises: 
Create Date: 2023-12-26 18:34:21.533356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed24bcd25885'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=100), nullable=True),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('birth_year', sa.Integer(), nullable=True),
    sa.Column('gender', sa.String(length=50), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('skin_color', sa.String(length=100), nullable=True),
    sa.Column('eye_color', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=100), nullable=True),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('diameter', sa.Integer(), nullable=True),
    sa.Column('gravity', sa.String(length=100), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.Column('climate', sa.String(length=100), nullable=True),
    sa.Column('terrain', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('last_name', sa.String(length=250), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('vehicles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=100), nullable=True),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('model', sa.String(length=100), nullable=True),
    sa.Column('vehicle_class', sa.String(length=100), nullable=True),
    sa.Column('passengers', sa.Integer(), nullable=True),
    sa.Column('manufacturer', sa.String(length=100), nullable=True),
    sa.Column('length', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('id_characters', sa.Integer(), nullable=True),
    sa.Column('id_planets', sa.Integer(), nullable=True),
    sa.Column('id_vehicles', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_characters'], ['characters.id'], ),
    sa.ForeignKeyConstraint(['id_planets'], ['planets.id'], ),
    sa.ForeignKeyConstraint(['id_vehicles'], ['vehicles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorites')
    op.drop_table('vehicles')
    op.drop_table('user')
    op.drop_table('planets')
    op.drop_table('characters')
    # ### end Alembic commands ###
