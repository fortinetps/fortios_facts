#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The module file for fortios_facts
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': [u'preview'],
                    'supported_by': 'network'}


DOCUMENTATION = """
---
module: fortios_facts
version_added: 2.2
short_description: Get facts about fortios devices.
extends_documentation_fragment: fortios
description:
  - Collects facts from network devices running the fortios operating
    system. This module places the facts gathered in the fact tree keyed by the
    respective resource name.  The facts module will always collect a
    base set of facts from the device and can enable or disable
    collection of additional facts.
author:
  - Ricardo Carrillo Cruz (@rcarrillocruz)
  - Nilashish Chakraborty (@Nilashishc)
options:
  gather_subset:
    description:
      - When supplied, this argument will restrict the facts collected
        to a given subset.  Possible values for this argument include
        all, hardware, config, and interfaces.  Can specify a list of
        values to include a larger subset.  Values can also be used
        with an initial C(M(!)) to specify that a specific subset should
        not be collected.
    required: false
    default: '!config'
  gather_network_resources:
    description:
      - When supplied, this argument will restrict the facts collected
        to a given subset. Possible values for this argument include
        all and the resources like interfaces, lacp etc.
        Can specify a list of values to include a larger subset. Values
        can also be used with an initial C(M(!)) to specify that a
        specific subset should not be collected.
    required: false
    choices: ['all', 'lacp', '!lacp', 'lacp_interfaces', '!lacp_interfaces']
    version_added: "2.9"
"""

EXAMPLES = """
# Gather all facts
- fortios_facts:
    gather_subset: all
    gather_network_resources: all

# Collect only the config and default facts
- fortios_facts:
    gather_subset:
      - config

# Do not collect hardware facts
- fortios_facts:
    gather_subset:
      - "!hardware"

# Collect only the lacp facts
- fortios_facts:
    gather_subset:
      - "!all"
      - "!min"
    gather_network_resources:
      - lacp

# Do not collect lacp_interfaces facts
- fortios_facts:
    gather_network_resources:
      - "!lacp_interfaces"

# Collect lacp and minimal default facts
- fortios_facts:
    gather_subset: min
    gather_network_resources: lacp
"""

RETURN = """
ansible_net_gather_subset:
  description: The list of fact subsets collected from the device
  returned: always
  type: list

# default
ansible_net_version:
  description: The operating system version running on the remote device
  returned: always
  type: str
ansible_net_hostname:
  description: The configured hostname of the device
  returned: always
  type: str
ansible_net_image:
  description: The image file the device is running
  returned: always
  type: str
ansible_net_api:
  description: The name of the transport
  returned: always
  type: str
ansible_net_python_version:
  description: The Python version Ansible controller is using
  returned: always
  type: str
ansible_net_model:
  description: The model name returned from the device
  returned: always
  type: str

# hardware
ansible_net_filesystems:
  description: All file system names available on the device
  returned: when hardware is configured
  type: list
ansible_net_memfree_mb:
  description: The available free memory on the remote device in Mb
  returned: when hardware is configured
  type: int
ansible_net_memtotal_mb:
  description: The total memory on the remote device in Mb
  returned: when hardware is configured
  type: int

# config
ansible_net_config:
  description: The current active config from the device
  returned: when config is configured
  type: str

# interfaces
ansible_net_all_ipv4_addresses:
  description: All IPv4 addresses configured on the device
  returned: when interfaces is configured
  type: list
ansible_net_all_ipv6_addresses:
  description: All IPv6 addresses configured on the device
  returned: when interfaces is configured
  type: list
ansible_net_interfaces:
  description: A hash of all interfaces running on the system
  returned: when interfaces is configured
  type: dict
ansible_net_neighbors:
  description: The list of LLDP neighbors from the remote device
  returned: when interfaces is configured
  type: dict

# network resources
ansible_net_gather_network_resources:
  description: The list of fact resource subsets collected from the device
  returned: always
  type: list
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible.module_utils.network.fortios.fortios import FortiOSHandler
from ansible.module_utils.network.fortimanager.common import FAIL_SOCKET_MSG
from ansible.module_utils.network.fortios.fortios import fortios_argument_spec
from ansible.module_utils.network.fortios.argspec.facts.facts import FactsArgs
from ansible.module_utils.network.fortios.facts.facts import Facts
from ansible.module_utils.six import iteritems


class Factbase(object):
    def __init__(self, module, fos, uri=None):
        self.module = module
        self.fos = fos
        self.uri = uri
        self.facts = dict()


class System(Factbase):
    def populate_facts(self):
        fos = self.fos
        vdom = 'root' #data['vdom']
        if self.uri.startswith(tuple(FACT_SYSTEM_SUBSETS)):
            resp = fos.monitor('system', self.uri[len('system_'):].replace('_','/'), vdom=vdom)
            self.facts.update({self.uri: resp})


def login(data, fos):
    host = data['host']
    username = data['username']
    password = data['password']
    ssl_verify = False #data['ssl_verify']

    fos.debug('on')
    if 'https' in data and not data['https']:
        fos.https('off')
    else:
        fos.https('on')

    fos.login(host, username, password, verify=ssl_verify)



FACT_SUBSETS = dict(
    system=System,
)
  
VALID_SUBSETS = frozenset(FACT_SUBSETS.keys())

FACT_SYSTEM_SUBSETS = frozenset([
    "system_firmware_select",
    "system_ha-checksums_select",
    "system_interface_select",
    "system_status_select"
])

def main():
    """
    Main entry point for module execution

    :returns: ansible_facts
    """
    spec = FactsArgs.argument_spec
    spec.update(fortios_argument_spec)

    module = AnsibleModule(argument_spec=spec,
                           supports_check_mode=False)
    # warnings = ['default value for `gather_subset` '
    #             'will be changed to `min` from `!config` v2.11 onwards']
  
    legacy_mode = 'host' in module.params and module.params['host'] is not None and \
                  'username' in module.params and module.params['username'] is not None and \
                  'password' in module.params and module.params['password'] is not None

    if not legacy_mode:
        if module._socket_path:
            connection = Connection(module._socket_path)
            fos = FortiOSHandler(connection)

            is_error, has_changed, result = fortios_user(module.params, fos)
        else:
            module.fail_json(**FAIL_SOCKET_MSG)
    else:
        try:
            from fortiosapi import FortiOSAPI
        except ImportError:
            module.fail_json(msg="fortiosapi module is required")

        fos = FortiOSAPI()

        login(module.params, fos)

        gather_subset = module.params['gather_subset']

        runable_subsets = set()
        exclude_subsets = set()
    
        for subset in gather_subset:
            if subset == 'all':
                runable_subsets.update(VALID_SUBSETS)
                continue
    
            if subset.startswith('!'):
                subset = subset[1:]
                if subset == 'all':
                    exclude_subsets.update(VALID_SUBSETS)
                    continue
                exclude = True
            else:
                exclude = False
            
            if not subset.startswith(tuple(VALID_SUBSETS)):
                module.fail_json(msg='Subset must be one of [%s], got %s' %
                                 (', '.join(VALID_SUBSETS), subset))
    
            if exclude:
                for valid_subset in VALID_SUBSETS:
                    if subset.startswith(valid_subset):
                        exclude_subsets.add({subset: valid_subset})
            else:
                for valid_subset in VALID_SUBSETS:
                    if subset.startswith(valid_subset):
                        runable_subsets.add((subset, valid_subset))
    
        if not runable_subsets:
            runable_subsets.update(VALID_SUBSETS)
    
        runable_subsets.difference_update(exclude_subsets)
        # runable_subsets.add('system')
    
        facts = dict()
        facts['gather_subset'] = list(runable_subsets)
    
        # Create instance classes, e.g. System, Session etc.
        instances = list()
    
        for (subset, valid_subset) in runable_subsets:
            instances.append(FACT_SUBSETS[valid_subset](module, fos, subset))
    
        # Populate facts for instances
        for inst in instances:
            inst.populate_facts()
            facts.update(inst.facts)

        fos.logout()
    
        ansible_facts = dict()
    
        for key, value in iteritems(facts):
            # key = 'ansible_net_%s' % key
            key = key
            ansible_facts[key] = value
    
        module.exit_json(ansible_facts=ansible_facts)
    

if __name__ == '__main__':
    main()