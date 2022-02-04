"""Add workflow_type  attribute

Revision ID: 5491d30e4ebb
Revises: 7d5de0772a10
Create Date: 2022-02-02 13:19:55.175483

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5491d30e4ebb'
down_revision = '7d5de0772a10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_full_name'), 'user', ['full_name'], unique=False)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.add_column('workflow', sa.Column('title', sa.String(), nullable=True))
    op.add_column('workflow', sa.Column('workflow_type', sa.String(), nullable=True))
    op.drop_index('ix_workflow_name', table_name='workflow')
    op.create_index(op.f('ix_workflow_title'), 'workflow', ['title'], unique=False)
    op.drop_column('workflow', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('workflow', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_workflow_title'), table_name='workflow')
    op.create_index('ix_workflow_name', 'workflow', ['name'], unique=False)
    op.drop_column('workflow', 'workflow_type')
    op.drop_column('workflow', 'title')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_full_name'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
