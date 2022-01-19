"""Add Job model

Revision ID: f1a29cfdc28a
Revises: 0f06ca144817
Create Date: 2021-12-28 10:08:28.364282

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f1a29cfdc28a'
down_revision = '0f06ca144817'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('workflow',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('workflow', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workflow_description'), 'workflow', ['description'], unique=False)
    op.create_index(op.f('ix_workflow_id'), 'workflow', ['id'], unique=False)
    op.create_index(op.f('ix_workflow_title'), 'workflow', ['title'], unique=False)
    op.add_column('job', sa.Column('id', sa.Integer(), nullable=False))
    op.add_column('job', sa.Column('workflow_id', sa.Integer(), nullable=True))
    op.add_column('job', sa.Column('workflow_type', sa.String(), nullable=True))
    op.add_column('job', sa.Column('workflow_execute_at', sa.TIMESTAMP(), nullable=True))
    op.drop_index('ix_job_uuid', table_name='job')
    op.create_index(op.f('ix_job_id'), 'job', ['id'], unique=False)
    op.create_index(op.f('ix_job_workflow_execute_at'), 'job', ['workflow_execute_at'], unique=False)
    op.create_index(op.f('ix_job_workflow_type'), 'job', ['workflow_type'], unique=False)
    op.create_foreign_key(None, 'job', 'workflow', ['workflow_id'], ['id'])
    op.drop_column('job', 'uuid')
    op.drop_column('job', 'flow')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job', sa.Column('flow', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.add_column('job', sa.Column('uuid', postgresql.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'job', type_='foreignkey')
    op.drop_index(op.f('ix_job_workflow_type'), table_name='job')
    op.drop_index(op.f('ix_job_workflow_execute_at'), table_name='job')
    op.drop_index(op.f('ix_job_id'), table_name='job')
    op.create_index('ix_job_uuid', 'job', ['uuid'], unique=False)
    op.drop_column('job', 'workflow_execute_at')
    op.drop_column('job', 'workflow_type')
    op.drop_column('job', 'workflow_id')
    op.drop_column('job', 'id')
    op.drop_index(op.f('ix_workflow_title'), table_name='workflow')
    op.drop_index(op.f('ix_workflow_id'), table_name='workflow')
    op.drop_index(op.f('ix_workflow_description'), table_name='workflow')
    op.drop_table('workflow')
    # ### end Alembic commands ###
