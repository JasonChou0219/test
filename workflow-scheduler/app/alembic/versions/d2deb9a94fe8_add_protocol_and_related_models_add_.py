"""Add protocol and related models, add list of protocol and database ids to job models

Revision ID: d2deb9a94fe8
Revises: 41e148b94e50
Create Date: 2022-03-11 15:00:01.871156

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd2deb9a94fe8'
down_revision = '41e148b94e50'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('protocol',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('owner', sa.String(), nullable=True),
    sa.Column('owner_id', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_protocol_id'), 'protocol', ['id'], unique=False)
    op.create_index(op.f('ix_protocol_owner'), 'protocol', ['owner'], unique=False)
    op.create_index(op.f('ix_protocol_owner_id'), 'protocol', ['owner_id'], unique=False)
    op.create_index(op.f('ix_protocol_title'), 'protocol', ['title'], unique=False)
    op.create_table('protocolservice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(), nullable=True),
    sa.Column('protocol_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['protocol_id'], ['protocol.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_protocolservice_id'), 'protocolservice', ['id'], unique=False)
    op.create_index(op.f('ix_protocolservice_uuid'), 'protocolservice', ['uuid'], unique=False)
    op.create_table('feature',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('identifier', sa.String(), nullable=True),
    sa.Column('service_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['service_id'], ['protocolservice.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_feature_id'), 'feature', ['id'], unique=False)
    op.create_index(op.f('ix_feature_identifier'), 'feature', ['identifier'], unique=False)
    op.create_table('command',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('identifier', sa.String(), nullable=True),
    sa.Column('observable', sa.Boolean(), nullable=True),
    sa.Column('meta', sa.Boolean(), nullable=True),
    sa.Column('interval', sa.Integer(), nullable=True),
    sa.Column('feature_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['feature_id'], ['feature.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_command_id'), 'command', ['id'], unique=False)
    op.create_index(op.f('ix_command_identifier'), 'command', ['identifier'], unique=False)
    op.create_table('property',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('identifier', sa.String(), nullable=True),
    sa.Column('observable', sa.Boolean(), nullable=True),
    sa.Column('meta', sa.Boolean(), nullable=True),
    sa.Column('interval', sa.Integer(), nullable=True),
    sa.Column('feature_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['feature_id'], ['feature.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_property_id'), 'property', ['id'], unique=False)
    op.create_index(op.f('ix_property_identifier'), 'property', ['identifier'], unique=False)
    op.create_table('parameter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('identifier', sa.String(), nullable=True),
    sa.Column('command_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['command_id'], ['command.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_parameter_id'), 'parameter', ['id'], unique=False)
    op.create_index(op.f('ix_parameter_identifier'), 'parameter', ['identifier'], unique=False)
    op.create_table('response',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('identifier', sa.String(), nullable=True),
    sa.Column('command_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['command_id'], ['command.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_response_id'), 'response', ['id'], unique=False)
    op.create_index(op.f('ix_response_identifier'), 'response', ['identifier'], unique=False)
    op.add_column('job', sa.Column('list_protocol_and_database', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('scheduledjob', sa.Column('list_protocol_and_database', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('scheduledjob', 'list_protocol_and_database')
    op.drop_column('job', 'list_protocol_and_database')
    op.drop_index(op.f('ix_response_identifier'), table_name='response')
    op.drop_index(op.f('ix_response_id'), table_name='response')
    op.drop_table('response')
    op.drop_index(op.f('ix_parameter_identifier'), table_name='parameter')
    op.drop_index(op.f('ix_parameter_id'), table_name='parameter')
    op.drop_table('parameter')
    op.drop_index(op.f('ix_property_identifier'), table_name='property')
    op.drop_index(op.f('ix_property_id'), table_name='property')
    op.drop_table('property')
    op.drop_index(op.f('ix_command_identifier'), table_name='command')
    op.drop_index(op.f('ix_command_id'), table_name='command')
    op.drop_table('command')
    op.drop_index(op.f('ix_feature_identifier'), table_name='feature')
    op.drop_index(op.f('ix_feature_id'), table_name='feature')
    op.drop_table('feature')
    op.drop_index(op.f('ix_protocolservice_uuid'), table_name='protocolservice')
    op.drop_index(op.f('ix_protocolservice_id'), table_name='protocolservice')
    op.drop_table('protocolservice')
    op.drop_index(op.f('ix_protocol_title'), table_name='protocol')
    op.drop_index(op.f('ix_protocol_owner_id'), table_name='protocol')
    op.drop_index(op.f('ix_protocol_owner'), table_name='protocol')
    op.drop_index(op.f('ix_protocol_id'), table_name='protocol')
    op.drop_table('protocol')
    # ### end Alembic commands ###