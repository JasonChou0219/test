"""fix init_db

Revision ID: 3e71ddac285d
Revises: 5ddd1d2095ae
Create Date: 2022-02-02 13:36:11.177334

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e71ddac285d'
down_revision = '5ddd1d2095ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('workflow',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('workflow_type', sa.String(), nullable=True),
    sa.Column('file_name', sa.String(), nullable=True),
    sa.Column('data', sa.Text(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('owner', sa.String(), nullable=True),
    sa.Column('owner_id', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workflow_description'), 'workflow', ['description'], unique=False)
    op.create_index(op.f('ix_workflow_file_name'), 'workflow', ['file_name'], unique=False)
    op.create_index(op.f('ix_workflow_id'), 'workflow', ['id'], unique=False)
    op.create_index(op.f('ix_workflow_owner'), 'workflow', ['owner'], unique=False)
    op.create_index(op.f('ix_workflow_owner_id'), 'workflow', ['owner_id'], unique=False)
    op.create_index(op.f('ix_workflow_title'), 'workflow', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_workflow_title'), table_name='workflow')
    op.drop_index(op.f('ix_workflow_owner_id'), table_name='workflow')
    op.drop_index(op.f('ix_workflow_owner'), table_name='workflow')
    op.drop_index(op.f('ix_workflow_id'), table_name='workflow')
    op.drop_index(op.f('ix_workflow_file_name'), table_name='workflow')
    op.drop_index(op.f('ix_workflow_description'), table_name='workflow')
    op.drop_table('workflow')
    # ### end Alembic commands ###
