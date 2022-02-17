"""Add job_id to model and schema

Revision ID: 41e148b94e50
Revises: 5f142c9e534d
Create Date: 2022-02-16 15:35:24.668288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41e148b94e50'
down_revision = '5f142c9e534d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scheduledjob', sa.Column('job_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('scheduledjob', 'job_id')
    # ### end Alembic commands ###