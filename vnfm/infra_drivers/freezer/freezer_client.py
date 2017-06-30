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
    def __init__(self,auth_attr,region_name):

        print("#$############################################### 6.5 Freezer init#############################")
        print("#$############################################### 6.5 Freezer init#############################")
        self.keystone = OpenstackClients(auth_attr, region_name).keystone_session
        print("self.keystone.auth_token ",self.keystone.get_token())

        print("#$############################################### 6.5 Freezer init#############################")
        print("#$############################################### 6.5 Freezer init#############################")
        print("#$############################################### 6.5 Freezer init#############################")
        print("\n")
        print("\n")
        print("\n")
        self.auth_token = self.keystone.get_token()
        self.auth_attr = auth_attr
        print("#$############################################### 6.5 Freezer init#############################")
        print("\n")
        print("\n")
        print("\n")
        print("auth_attr ", self.auth_attr)
        print("#$############################################### 6.5 Freezer init#############################")
        print("\n")
        print("\n")
        print("\n")

        self.endpoint = self.keystone.get_endpoint(
            service_type='backup', region_name=None)

        print("self.endpoint ",self.endpoint)

        print("#$############################################### 6.5 Freezer init endpoint#############################")
        self.client = freezerclient.Client(token=self.auth_token, username=self.auth_attr['username'], password=self.auth_attr['password'],
                          tenant_name=self.auth_attr['project_name'], auth_url=self.auth_attr['auth_url'],
                          session=self.keystone.session,
                          endpoint=self.endpoint, opts=None, project_name='admin', user_domain_name='Default',
                          project_domain_name='Default', verify=True,cert=None)


    def get_client(self):
        return self.client


    def create(self):
        print("\n")
        print("\n")
        print("\n")
        print("#######################################################")
        print("#######################################################")
        print("#######################################################")
        print("#######################################################")
        print("############### create in freezer_client : 7")
        print("#######################################################")
        print("#######################################################")
        print("#######################################################")
        print("#######################################################")
        print("\n")
        print("Here is Function Freezer !!!!!!!!! 2017.06.29############")
