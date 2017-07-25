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

from oslo_log import log as logging
from oslo_utils import timeutils

from tacker.db.common_services import common_services_db
from tacker.plugins.common import constants
from tacker.vnfm.policy_actions import abstract_action
from tacker.vnfm import vim_client
from tacker.nfvo.drivers.vim import openstack_driver
from novaclient import client
from keystoneauth1 import session
from keystoneauth1.identity import v3
import time

LOG = logging.getLogger(__name__)


def _log_monitor_events(context, vnf_dict, evt_details):
    _cos_db_plg = common_services_db.CommonServicesPluginDb()
    _cos_db_plg.create_event(context, res_id=vnf_dict['id'],
                             res_type=constants.RES_TYPE_VNF,
                             res_state=vnf_dict['status'],
                             evt_type=constants.RES_EVT_MONITOR,
                             tstamp=timeutils.utcnow(),
                             details=evt_details)



cnt =0

class VNFActionRecovery(abstract_action.AbstractPolicyAction):
    def get_type(self):
        return 'recovery'

    def get_name(self):
        return 'recovery'

    def get_description(self):
        return 'Tacker VNF respawning policy'

    def execute_action(self, plugin, context, vnf_dict, args):
        global cnt
        print("\n")
        print("\n")
        print("\n")
        print("###########Called execute_action in recovery.py ##############")
        print("###########Called execute_action in recovery.py ##############")
        print("###########Called execute_action in recovery.py ##############")
        print("context",context)
        print("args is ",args)
        print("vnf_dict ",vnf_dict)
        print("\n")
        print("\n")

        def _fetch_vim(vim_uuid):
            return vim_client.VimClient().get_vim(context, vim_uuid)

        vnf_id = vnf_dict['id']
        attributes = vnf_dict['attributes']
        vim_id = vnf_dict['vim_id']





        print("################ vim_id ##############",vim_id)

        ##########recovery Step 1. create job and start rstore##############
        ##########recovery Step 1. create job and start rstore##############
        ##########recovery Step 1. create job and start rstore##############

        vim_res = _fetch_vim(vim_id)

        auth = v3.Password(auth_url=vim_res['vim_auth']['auth_url'], username=vim_res['vim_auth']['username']
                           , password=vim_res['vim_auth']['password'],
                           project_name=vim_res['vim_auth']['project_name'],
                           user_domain_id=vim_res['vim_auth']['user_domain_name'],
                           project_domain_id=vim_res['vim_auth']['project_domain_name'])
        sess = session.Session(auth=auth)
        novaclient = client.Client("2.1", session=sess)

        ip = vnf_dict['mgmt_url'].split(':')
        ###### ALL network Search

        ############################### Need Sujung ################################



        new_ip = ip[1].replace("}", "")

        result_ip = (new_ip.replace("\"", "")).strip()

        novadict = novaclient.servers.list(search_opts={'ip': str(result_ip)})
        novaname = novadict[0].name
        findnova = novaclient.servers.list(search_opts={'name': str(novaname)})

        for status in findnova :
            if  status.status == 'ACTIVE':
                print("NOOOOOOOOOOOOOOOOOOOOOPssssssss")
                print("status ",status.status)
                return

        if cnt == 0 :



            self.job_id = plugin._start_restore_action(context, vim_res['vim_auth'], vnf_dict['instance_id'])
            print(vim_res)
            print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXxx')
            print(vnf_dict)



            ############################### Need Sujung ################################
            ip = vnf_dict['mgmt_url'].split(':')
            ###### ALL network Search

            ############################### Need Sujung ################################


            while True:
                new_ip = ip[1].replace("}","")

                result_ip = (new_ip.replace("\"","")).strip()

                novadict = novaclient.servers.list(search_opts={'ip':str(result_ip)})
                novaname = novadict[0].name
                findnova=novaclient.servers.list(search_opts={'name':str(novaname)})


                self.newnova_ip = ""

                for novacls in findnova :
                    print("find nova name :",novacls.name)
                    print("find nova ip : ",novacls.addresses)
                    if novacls.status =='ACTIVE':
                        print("RESTORE NOVA IP type: ",type(novacls.addresses['net0'][0]))
                        print("RESTORE NOVA IP addr: ",str(novacls.addresses['net0'][0]['addr']))
                        self.newnova_ip = str(novacls.addresses['net0'][0]['addr'])
                        break



                if self.newnova_ip  !='':
                    break




            neutronclient = openstack_driver.NeutronClient(vim_res['vim_auth'])
            subnet_list =neutronclient.client.list_subnets()

            pool_list = neutronclient.client.list_lbaas_pools()
            print("#####################",pool_list)
            pool = pool_list['pools']

            subnet = subnet_list['subnets']
            print(subnet)

            for sub_id in  subnet:
                if str(sub_id['name']) =='net0':
                    self.subnet_id = sub_id['id']

            for pool_id in pool:
                if str(pool_id['name']) == 'test-lb-pool-socket':
                    self.pool_id = pool_id['id']




            kwargs = {
                'address': self.newnova_ip,
                'protocol_port': '18090',
                'admin_state_up': 'true',
                'subnet_id':self.subnet_id,
                'weight':1
            }

            print("#########################################")
            print("###########XXXXXXXXXXXXX#################")
            print("#########################################")
            print("#########################################")
            print("#########################################")

            res = neutronclient.client.create_lbaas_member(self.pool_id, {'member': kwargs})


            print("#########################################")
            print("###########createmembfeed#################")
            print("#########################################")
            print("#########################################")
            print("#########################################")


            print("############END RECOVERY#####################")

        cnt += 1








        # def _update_failure_count():
        #     failure_count = int(attributes.get('failure_count', '0')) + 1
        #     failure_count_str = str(failure_count)
        #     LOG.debug(_("vnf %(vnf_id)s failure count %(failure_count)s"),
        #               {'vnf_id': vnf_id, 'failure_count': failure_count_str})
        #     attributes['failure_count'] = failure_count_str
        #     attributes['dead_instance_id_' + failure_count_str] = vnf_dict[
        #         'instance_id']
        #

        #
        # def _delete_heat_stack(vim_auth):
        #     placement_attr = vnf_dict.get('placement_attr', {})
        #     region_name = placement_attr.get('region_name')
        #     heatclient = hc.HeatClient(auth_attr=vim_auth,
        #                                region_nam=region_name)
        #     heatclient.delete(vnf_dict['instance_id'])
        #     LOG.debug(_("Heat stack %s delete initiated"), vnf_dict[
        #         'instance_id'])
        #     _log_monitor_events(context, vnf_dict, "ActionespawnHeat invoked")
        #
        # def _respin_vnf():
        #     update_vnf_dict = plugin.create_vnf_sync(context, vnf_dict)
        #     LOG.info(_('respawned new vnf %s'), update_vnf_dict['id'])
        #     plugin.config_vnf(context, update_vnf_dict)
        #     return update_vnf_dict
        #
        #
        # if plugin._mark_vnf_dead(vnf_dict['id']):
        #     _update_failure_count()
        #     vim_res = _fetch_vim(vim_id)
        #     if vnf_dict['attributes'].get('monitoring_policy'):
        #         plugin._vnf_monitor.mark_dead(vnf_dict['id'])
        #         _delete_heat_stack(vim_res['vim_auth'])
        #         updated_vnf = _respin_vnf()
        #         plugin.add_vnf_to_monitor(context, updated_vnf)
        #         LOG.debug(_("VNF %s added to monitor thread"), updated_vnf[
        #             'id'])
        #     if vnf_dict['attributes'].get('alarming_policy'):
        #         _delete_heat_stack(vim_res['vim_auth'])
        #         vnf_dict['attributes'].pop('alarming_policy')
        #         _respin_vnf()


