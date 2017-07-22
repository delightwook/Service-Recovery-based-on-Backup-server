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


        if cnt == 0 :
            self.job_id = plugin._start_restore_action(context,vim_res['vim_auth'],vnf_dict['instance_id'])
            print(vim_res)
            print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXxx')
            print(vnf_dict)
            cnt += 1


        ##########recovery Step 2. create lb member##############
        # pool id
        #member
        #

        # 1. add member
        ### get new Nova IP address

        auth = v3.Password(auth_url=vim_res['vim_auth']['auth_url'],username=vim_res['vim_auth']['username']
                           ,password=vim_res['vim_auth']['password'],
                           project_name=vim_res['vim_auth']['project_name'],
                           user_domain_id=vim_res['vim_auth']['user_domain_name'],
                           project_domain_id=vim_res['vim_auth']['project_domain_name'])
        sess = session.Session(auth = auth)
        novaclient=client.Client("2.1",session=sess)


        ############################### Need Sujung ################################
        ip = vnf_dict['mgmt_url'].split(':')
        ###### ALL network Search

        ############################### Need Sujung ################################

        new_ip = ip[1].replace("}","")

        result_ip = (new_ip.replace("\"","")).strip()

        novadict = novaclient.servers.list(search_opts={'ip':str(result_ip)})

        # ListWithMetadata Tyoe

        novaname = novadict[0]
        novahead=novaclient.servers.get(novaname)
        print("#######################################################")
        print("#######################################################")
        print("#######################################################")
        print(type(novahead))
        print("#######################################################")
        print("##########s#############################################")
        print("#######################################################")
        print("#######################################################")



        # findnova = novaclient.servers.list(search_opts={'name':str(novaname)})



        #
        #neutronclient = openstack_drive
        # r.NeutronClient(vim_res['vim_auth'])
        #
        # creatmemfeed = neutronclient.client.create_lbaas_member('test-lb-pool-socket',)


        print("#########################################")
        print("###########createmembfeed#################")
        print("#########################################")
        print("#########################################")
        print("#########################################")











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
        #                                region_name=region_name)
        #     heatclient.delete(vnf_dict['instance_id'])
        #     LOG.debug(_("Heat stack %s delete initiated"), vnf_dict[
        #         'instance_id'])
        #     _log_monitor_events(context, vnf_dict, "ActionRespawnHeat invoked")
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


