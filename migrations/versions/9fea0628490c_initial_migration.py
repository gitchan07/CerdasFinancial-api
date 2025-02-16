"""initial migration

Revision ID: 9fea0628490c
Revises: 
Create Date: 2024-12-03 21:12:33.393932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fea0628490c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('full_name', sa.String(length=100), nullable=False),
    sa.Column('is_subscribe', sa.Integer(), nullable=True),
    sa.Column('subscribe_time', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('courses',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('detail', sa.Text(), nullable=True),
    sa.Column('video_url', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('created_by', sa.String(length=200), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('watchlist',
    sa.Column('id', sa.String(length=200), nullable=False),
    sa.Column('user_id', sa.String(length=200), nullable=False),
    sa.Column('course_id', sa.String(length=200), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('watchlist')
    op.drop_table('courses')
    op.drop_table('users')
    # ### end Alembic commands ###
