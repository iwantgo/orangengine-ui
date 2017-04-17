"""empty message

Revision ID: 85bba8d346c6
Revises: 83a4d5b6c9b8
Create Date: 2017-04-17 13:18:18.539889

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '85bba8d346c6'
down_revision = '83a4d5b6c9b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('device_profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('device_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['device.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('supplemental_device_param')
    op.add_column('zone_mapping', sa.Column('device_profile_id', sa.Integer(), nullable=True))
    op.drop_constraint(u'_zone_network_mapping_uc', 'zone_mapping', type_='unique')
    op.create_unique_constraint('_zone_network_mapping_uc', 'zone_mapping', ['device_profile_id', 'zone_name', 'network'])
    op.drop_constraint(u'zone_mapping_device_id_fkey', 'zone_mapping', type_='foreignkey')
    op.create_foreign_key(None, 'zone_mapping', 'device_profile', ['device_profile_id'], ['id'])
    op.drop_column('zone_mapping', 'device_id')
    op.add_column('zone_mapping_rules', sa.Column('device_profile_id', sa.Integer(), nullable=True))
    op.drop_constraint(u'zone_mapping_rules_device_id_source_zone_name_destination_n_key', 'zone_mapping_rules', type_='unique')
    op.create_unique_constraint(None, 'zone_mapping_rules', ['device_profile_id', 'source_zone_name', 'destination_network', 'destination_zone_name'])
    op.drop_constraint(u'zone_mapping_rules_device_id_fkey', 'zone_mapping_rules', type_='foreignkey')
    op.create_foreign_key(None, 'zone_mapping_rules', 'device_profile', ['device_profile_id'], ['id'])
    op.drop_column('zone_mapping_rules', 'device_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('zone_mapping_rules', sa.Column('device_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'zone_mapping_rules', type_='foreignkey')
    op.create_foreign_key(u'zone_mapping_rules_device_id_fkey', 'zone_mapping_rules', 'device', ['device_id'], ['id'])
    op.drop_constraint(None, 'zone_mapping_rules', type_='unique')
    op.create_unique_constraint(u'zone_mapping_rules_device_id_source_zone_name_destination_n_key', 'zone_mapping_rules', ['device_id', 'source_zone_name', 'destination_network', 'destination_zone_name'])
    op.drop_column('zone_mapping_rules', 'device_profile_id')
    op.add_column('zone_mapping', sa.Column('device_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'zone_mapping', type_='foreignkey')
    op.create_foreign_key(u'zone_mapping_device_id_fkey', 'zone_mapping', 'device', ['device_id'], ['id'])
    op.drop_constraint('_zone_network_mapping_uc', 'zone_mapping', type_='unique')
    op.create_unique_constraint(u'_zone_network_mapping_uc', 'zone_mapping', ['device_id', 'zone_name', 'network'])
    op.drop_column('zone_mapping', 'device_profile_id')
    op.create_table('supplemental_device_param',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('modified_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('deleted', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('value', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('device_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['device_id'], [u'device.id'], name=u'supplemental_device_param_device_id_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'supplemental_device_param_pkey'),
    sa.UniqueConstraint('device_id', 'name', name=u'_device_param_uc')
    )
    op.drop_table('device_profile')
    # ### end Alembic commands ###
