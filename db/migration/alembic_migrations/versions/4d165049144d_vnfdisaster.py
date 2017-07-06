# Copyright 2017 OpenStack Foundation
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

"""vnfdisaster

Revision ID: 4d165049144d
Revises: e7993093baf1
Create Date: 2017-07-06 21:12:27.444484

"""

# revision identifiers, used by Alembic.
revision = '4d165049144d'
down_revision = 'e7993093baf1'

from alembic import op
import sqlalchemy as sa


from tacker.db import migration


def upgrade(active_plugins=None, options=None):
    # job information and Status table
    op.create_table(
        'vnfjobinfo',
        sa.Column('job_id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=False),
        sa.Column('nova_instance_id', sa.String(length=48), nullable=False),
        sa.Column('tacker_instance_id', sa.String(length=48), nullable=False),
        sa.Column('action', sa.String(length=24), nullable=False),
        sa.Column('result', sa.String(length=24), nullable=False),
        sa.Column('status', sa.String(length=24), nullable=False),
        #    sa.PrimaryKeyConstraint('job_id'),
        mysql_engine='InnoDB'
    )
    # backup information and Status table
    op.create_table(
        'vnfbackup',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('tenant_id', sa.String(length=36), nullable=False),
        sa.Column('action', sa.String(length=24), nullable=False),
        sa.Column('container', sa.String(length=24), nullable=False),
        sa.Column('storage', sa.String(length=36), nullable=False),
        sa.Column('backup_name', sa.String(length=255), nullable=False),
        sa.Column('nova_instance_id', sa.String(length=48), nullable=False),
        sa.Column('job_id', sa.String(length=36), default='', nullable=False),
        sa.Column('start_time', sa.String(length=48), nullable=False),
        sa.Column('end_time', sa.String(length=48), nullable=False),
        sa.Column('interval', sa.String(length=48), nullable=False),
      #  sa.ForeignKeyConstraint(['job_id'], ['vnfjobinfo.job_id'], ),
        sa.PrimaryKeyConstraint('id'),
        mysql_engine='InnoDB'
    )
    # restroe information and Status table
    op.create_table(
        'vnfrestore',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('tenant_id', sa.String(length=36), nullable=False),
        sa.Column('action', sa.String(length=24), nullable=False),
        sa.Column('container', sa.String(length=24), nullable=False),
        sa.Column('storage', sa.String(length=36), nullable=False),
        sa.Column('backup_name', sa.String(length=255), nullable=False),
        sa.Column('nova_instance_id', sa.String(length=48), nullable=False),
        sa.Column('neutron_network_id', sa.String(length=48), nullable=False),
        sa.Column('job_id', sa.String(length=36), nullable=False),
      #  sa.ForeignKeyConstraint(['job_id'], ['vnfjobinfo.job_id'], ),
        sa.PrimaryKeyConstraint('id'),
        mysql_engine='InnoDB'
    )


