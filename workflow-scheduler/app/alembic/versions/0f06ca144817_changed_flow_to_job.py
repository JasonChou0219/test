"""Changed flow to job

Revision ID: 0f06ca144817
Revises: 5d8ffb895d68
Create Date: 2021-10-22 13:15:36.016158

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0f06ca144817'
down_revision = '5d8ffb895d68'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job',
    sa.Column('uuid', postgresql.UUID(), nullable=False),
    sa.Column('flow', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('execute_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_job_created_at'), 'job', ['created_at'], unique=False)
    op.create_index(op.f('ix_job_description'), 'job', ['description'], unique=False)
    op.create_index(op.f('ix_job_execute_at'), 'job', ['execute_at'], unique=False)
    op.create_index(op.f('ix_job_title'), 'job', ['title'], unique=False)
    op.create_index(op.f('ix_job_uuid'), 'job', ['uuid'], unique=False)
    op.drop_index('ix_flow_description', table_name='flow')
    op.drop_index('ix_flow_id', table_name='flow')
    op.drop_table('flow')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('flow',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('flow', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], name='flow_owner_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='flow_pkey')
    )
    op.create_index('ix_flow_id', 'flow', ['id'], unique=False)
    op.create_index('ix_flow_description', 'flow', ['description'], unique=False)
    op.drop_index(op.f('ix_job_uuid'), table_name='job')
    op.drop_index(op.f('ix_job_title'), table_name='job')
    op.drop_index(op.f('ix_job_execute_at'), table_name='job')
    op.drop_index(op.f('ix_job_description'), table_name='job')
    op.drop_index(op.f('ix_job_created_at'), table_name='job')
    op.drop_table('job')
    # ### end Alembic commands ###