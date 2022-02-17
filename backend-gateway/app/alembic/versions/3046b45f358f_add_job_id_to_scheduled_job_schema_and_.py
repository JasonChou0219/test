"""Add job_id to scheduled job schema and model

Revision ID: 3046b45f358f
Revises: 958b889299b4
Create Date: 2022-02-16 15:32:48.532068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3046b45f358f'
down_revision = '958b889299b4'
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