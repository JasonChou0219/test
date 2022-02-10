"""Add workflow_type attribute

Revision ID: c5fa78dcf257
Revises: 1363ee1f3b3b
Create Date: 2022-02-02 13:21:31.845463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5fa78dcf257'
down_revision = '1363ee1f3b3b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('workflow', sa.Column('title', sa.String(), nullable=True))
    op.add_column('workflow', sa.Column('workflow_type', sa.String(), nullable=True))
    op.drop_index('ix_workflow_name', table_name='workflow')
    op.create_index(op.f('ix_workflow_title'), 'workflow', ['title'], unique=False)
    op.create_index(op.f('ix_workflow_workflow_type'), 'workflow', ['workflow_type'], unique=False)
    op.drop_column('workflow', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('workflow', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_workflow_workflow_type'), table_name='workflow')
    op.drop_index(op.f('ix_workflow_title'), table_name='workflow')
    op.create_index('ix_workflow_name', 'workflow', ['name'], unique=False)
    op.drop_column('workflow', 'workflow_type')
    op.drop_column('workflow', 'title')
    # ### end Alembic commands ###