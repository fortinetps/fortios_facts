#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The arg spec for the iosxr facts module.
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class FactsArgs(object):  # pylint: disable=R0903
    """ The arg spec for the iosxr facts module
    """

    def __init__(self, **kwargs):
        pass

    choices = [
        'all',
        'endpoint-control',
        'extender-controller',
        'firewall',
        'firewall_policy_select',
        'firewall_session_select',
        'fortiview',
        'geoip',
        'ips',
        'license',
        'log',
        'registration',
        'router',
        'switch-controller',
        'system',
        'system_current-admins_select',
        'system_debug_download'
        'system_firmware_select',
        'system_fortimanager_status',
        'system_ha-checksums_select',
        'system_interface_select',
        'system_status_select',
        'system_time_select',
        'system_timezong_select',
        'user',
        'user_device_select',
        'utm',
        'virtual-wan',
        'vpn',
        'vpn-certificate',
        'wanopt',
        'webcache',
        'webfilter',
        'webproxy',
        'wifi'
    ]

    argument_spec = {
        'gather_subset': dict(default=['system'], type='list'),
        'gather_network_resources': dict(choices=choices, type='list'),
    }