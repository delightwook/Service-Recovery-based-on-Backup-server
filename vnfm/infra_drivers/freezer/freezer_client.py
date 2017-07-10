# Copyright 2013, 2014 Intel Corporation.
# All Rights Reserved.
#
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


from freezerclient.v1 import client as freezerclient
from tacker.common.clients import OpenstackClients

class FreezerClient(object):
    #### Freezer Client #####
    def __init__(self,auth_attr,action_info,region_name=None,):
        self.keystone = OpenstackClients(auth_attr, region_name).keystone_session
        self.auth_token = self.keystone.get_token()
        self.action_info = action_info
        self.auth_attr = auth_attr
        self.endpoint = self.keystone.get_endpoint(
            service_type='backup', region_name=None)



        self.client = freezerclient.Client(token=self.auth_token, username=self.auth_attr['username'], password=self.auth_attr['password'],
                          tenant_name=self.auth_attr['project_name'], auth_url=self.auth_attr['auth_url'],
                          session=self.keystone,
                          endpoint=self.endpoint, opts=None, project_name='admin', user_domain_name='Default',
                          project_domain_name='Default', verify=True,cert=None)


    def get_client(self):
        return self.client





    def _create_doc(self,action_info):
        doc ={}


        if action_info['action'] == 'backup':

            doc['description'] = "TEST-BACKUP"

            freezer_action= {'freezer_action':{'backup_name': self.action_info['name'],
                             'container' : self.action_info['container'],
                             'storage':self.action_info['storage'],'snapshot' :False,
                             'mode' : 'nova','action': self.action_info['action'],
                             'log_file' : '/root/test/freezerlog.log',
                             'nova_inst_id' : self.action_info['nova_instance_id']}}

            doc['job_actions'] = [freezer_action,]
            doc['job_schedule'] = {'schedule_interval' : self.action_info['interval']+' minutes',
                                   'schedule_end_date':self.action_info['end_time'],
                                   'schedule_start_date' : self.action_info['start_time'],
                                   'result' : 'success','event':'start','status' : 'stop'}

        elif action_info['action'] =='restore':
            doc['description'] = "TEST-restore"

            freezer_action = {'freezer_action': {'backup_name': self.action_info['name'],
                                                 'container': self.action_info['container'],
                                                 'storage': self.action_info['storage'], 'snapshot': False,
                                                 'mode': 'nova', 'action': self.action_info['action'],
                                                 'log_file': '/root/test/freezerlog.log',
                                                 'nova_restore_network':self.action_info['neutron_network_id'],
                                                 'nova_inst_id': self.action_info['nova_instance_id']}}

            doc['job_actions'] = [freezer_action, ]
            doc['job_schedule'] = {'result': 'success', 'event': '', 'status': 'stop'}

        return doc


    def create(self):
        doc = self._create_doc(self.action_info)
        print('##########################################')
        print('##########################################')
        print('##########################################',doc)
        jobs = self.client.jobs.create(doc)
        return jobs














