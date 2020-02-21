#!/usr/bin/env python3
import os
import re
import sys
import time
import json
import argparse
import threading
from jsondiff import diff
from pyeapi import load_config
from pyeapi import connect_to
from plugins.acl import acl
from plugins.as_path import as_path
from plugins.bgp_evpn import bgp_evpn
from plugins.bgp_ipv4 import bgp_ipv4
from plugins.interface import interface
from plugins.ip_route import ip_route
from plugins.mlag import mlag
from plugins.ntp import ntp
from plugins.prefix_list import prefix_list
from plugins.route_map import route_map
from plugins.snmp import snmp
from plugins.stp import stp
from plugins.vlan import vlan
from plugins.vrf import vrf
from plugins.vxlan import vxlan

def arguments():
    parser = argparse.ArgumentParser(
        prog='pyATEOS',
        description='''pyATEOS - A simple python application for operational status test on 
        Arista device. Based on pyATS idea and pyeapi library for API calls.'''
        )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-B',
        '--before',
        dest='before',
        action='store_true',
        help='''write json file containing the test result BEFORE. 
        To be run BEFORE the config change. 
        File path example: $PWD/before/ntp/router1_ntp.json'''
        )
    group.add_argument(
        '-A',
        '--after',
        dest='after',
        action='store_true',
        help='''write json file containing the test result AFTER. 
        To be run AFTER the config change. 
        File path example: $PWD/after/ip_route/router1_ip_route.json'''
        )
    group.add_argument(
        '-C',
        '--compare',
        dest='compare',
        action='store_true',
        help='''diff between before and after test files.
        File path example: $PWD/diff/snmp/router1_snmp.json'''
        )
    parser.add_argument(
        '-i',
        '--inventory',
        dest='inventory',
        help='specify pyeapi inventory file path'
        )
    parser.add_argument(
        '-n',
        '--node',
        dest='node',
        help='specify inventory node. Multiple values are accepted separated by space',
        nargs='+',
        required=True
        )
    parser.add_argument(
        '-t',
        '--test',
        dest='test',
        help='run one or more specific test. Multiple values are accepted separated by space',
        nargs='+',           
        required=True
        )

    return parser.parse_args()


def flags(args):

    returned_dict = dict()

    if args.inventory:
        inventory = args.inventory
    else:
        inventory = 'eos_inventory.ini'

    returned_dict.update(
        inventory=inventory,
        node=args.node,
        test=args.test,
        before=args.before,
        after=args.after,
        compare=args.compare,
        )

    return returned_dict


class WriteFile():
    def __init__(self, test, node):

        self.test = test
        self.node = node
        self.pwd_before = os.getcwd() + '/before/{}'.format(self.test)
        self.pwd_after = os.getcwd() + '/after/{}'.format(self.test)
        self.pwd_diff = os.getcwd() + '/diff/{}'.format(self.test)

    def write_before(self, result):
        if not os.path.exists(self.pwd_before) :
            os.makedirs(self.pwd_before)

        with open('{}/{}_{}.json'.format(self.pwd_before, self.test, self.node), 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=4)


    def write_after(self, result):
        if not os.path.exists(self.pwd_after):
            os.makedirs(self.pwd_after)

        with open('{}/{}_{}.json'.format(self.pwd_after, self.test, self.node), 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=4)


    def write_diff(self):

        if not os.path.exists(self.pwd_diff) :
            os.makedirs(self.pwd_diff)  
        
        def replace(string, substitutions):

            substrings = sorted(substitutions, key=len, reverse=True)
            regex = re.compile('|'.join(map(re.escape, substrings)))

            return regex.sub(lambda match: substitutions[match.group(0)], string)

        substitutions = {
            '\'':'\"', 
            'insert':'"insert"', 
            'delete':'"delete"', 
            'True':'true', 
            'False':'false',
            '(':'[',
            ')':']',
            }

        try:
            before = open('{}/{}_{}.json'.format(self.pwd_before, self.test, self.node), 'r')
        except FileNotFoundError as error:
            print(error)
            sys.exit(1)
        
        try:
            after = open('{}/{}_{}.json'.format(self.pwd_after, self.test, self.node), 'r')
        except FileNotFoundError as error:
            print(error)        
            sys.exit(1)
        
        json_diff = str(diff(before, after, load=True, syntax='symmetric'))
        edit_json_diff = replace(json_diff, substitutions)
        final_diff = json.loads(edit_json_diff)

        with open('{}/{}_{}.json'.format(self.pwd_diff, self.test, self.node), 'w', encoding='utf-8') as file:
            json.dump(final_diff, file, ensure_ascii=False, indent=4)

# def thread_node(nodes):
#     node_threads = list()
#     for node in nodes:
#         thread_targets = threading.Thread(target=influxdb_call, args=(node))
#         thread_targets.start()
#         node_threads.append(thread_targets)

def bef_aft_com(node, test, before=None, after=None, compare=None):

    test_run = list()
    test_all = [
        'acl',
        'as_path',
        'bgp_evpn',
        'bgp_ipv4',
        'interface',
        'ip_route',
        'mlag',
        'ntp',
        'prefix_list',
        'route_map',
        'snmp',
        'stp',
        'vlan',
        'vrf',
        'vxlan'
    ]

    if 'mgmt' in test:
        test.remove('mgmt')
        test_run.extend(('ntp','snmp'))
    elif 'routing' in test:
        test.remove('routing')
        test_run.extend(('bgp_evpn','bgp_ipv4','ip_route'))
    elif 'layer2' in test:
        test.remove('layer2')
        test_run.extend(('stp','vlan','vxlan'))
    elif 'ctrl' in test:
        test.remove('ctrl')
        test_run.extend(('acl','as_path','prefix_list','route_map'))
    elif 'all' in test:
        test.remove('all')
        test_run = test_all

    test_run.extend(test)

    for test in list(set(test_run)):
        if before:
            wr_before = WriteFile(test, node)
            wr_before.write_before(eval(test)(connect_to(node)).show)
        elif after:
            wr_after = WriteFile(test, node)
            wr_after.write_after(eval(test)(connect_to(node)).show)
        elif compare:
            wr_diff = WriteFile(test, node)
            wr_diff.write_diff()
    

def main():

    my_flags = flags(arguments())

    inventory = my_flags.get('inventory')
    node = my_flags.get('node')    
    test = my_flags.get('test')
    before = my_flags.get('before')
    after = my_flags.get('after')
    compare = my_flags.get('compare')

    load_inventory = load_config(inventory)
    
    if test:
        for node in node:
            bef_aft_com(node, test, before, after, compare)


if __name__ == '__main__':
    main()
