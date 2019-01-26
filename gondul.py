#!/usr/bin/env python

import argparse
import json
import requests

def parse_args():
    '''
    This function parses the arguments that were passed in via the command line.
    This function expects no arguments.
    '''

    parser = argparse.ArgumentParser(description='Ansible Gondul '
                                     'inventory module')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true',
                       help='List active switches')
    group.add_argument('--host', help='List details about the specified switch')

    return parser.parse_args()

def list_switches():
    r = requests.get('http://10.10.2.20/api/read/switches-management')
    switches = r.json()['switches']
    hostsvars = {}
    hosts = []
    for switch_name in switches:
        switch = switches[switch_name]
        hostvar = {
            'distro_name': switch['distro_name'],
            'distro_phy_port': switch['distro_phy_port'],
            'subnet4': switch['subnet4'],
            'subnet6': switch['subnet6'],
            'community': switch['community'],
            'sysname': switch['sysname'],
            'mgmt_v4_addr': switch['mgmt_v4_addr'],
            'mgmt_v6_addr': switch['mgmt_v6_addr'],
            'traffic_vlan': switch['traffic_vlan'],
            'ansible_host': switch['mgmt_v4_addr'],
            'ansible_network_os': 'junos',
            'host': switch['mgmt_v4_addr']
        }
        hostsvars.update({switch['sysname']: hostvar})
        hosts.append(switch['sysname'])

    inventory = {
    "_meta": hostsvars,
    "switches": {"hosts": hosts}
    }

    inv_string = json.dumps(inventory, indent=1, sort_keys=True)
    print(inv_string)

def get_host_attributes(host):
    r = requests.get('http://10.10.2.20/api/read/switches-management')
    switches = r.json()['switches']
    if host not in switches:
        print(json.dumps({}, indent=1, sort_keys=True))
        return

    switch = switches[host]
    hostvar = {
        'distro_name': switch['distro_name'],
        'distro_phy_port': switch['distro_phy_port'],
        'subnet4': switch['subnet4'],
        'subnet6': switch['subnet6'],
        'community': switch['community'],
        'sysname': switch['sysname'],
        'mgmt_v4_addr': switch['mgmt_v4_addr'],
        'mgmt_v6_addr': switch['mgmt_v6_addr'],
        'traffic_vlan': switch['traffic_vlan'],
        'ansible_host': switch['mgmt_v4_addr'],
        'ansible_network_os': 'junos',
        'host': switch['mgmt_v4_addr']
    }
    inv_string = json.dumps(hostvar, indent=1, sort_keys=True)
    print(inv_string)

if __name__ == '__main__':
    args = parse_args()

    if args.host:
        get_host_attributes(args.host)
    elif args.list:
        list_switches()