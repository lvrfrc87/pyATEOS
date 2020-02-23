#!/usr/bin/env python3
import os
import re
import sys
import time
import json
import argparse
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
    parser.add_argument(
        '-F',
        '--file_name',
        dest='file',
        help='''provide the 2 filename IDs to compare, separated by space. 
        BEFORE first, AFTER second. i.e [..] -C -f 1582386835 1582387929''',
        nargs='+',
        type=int,
        )

    if parser.parse_args().compare and parser.parse_args().file is None:
        parser.error("-C/--compare requires -F/--file_name.")

    return parser.parse_args()


def flags(args):
    returned_dict = dict()

    if args.inventory:
        inventory = args.inventory
    else:
        inventory = 'eos_inventory.ini'

    if args.compare:
        if args.file:
            assert len(args.file) == 2 and (args.file[0] - args.file[1]) < 0,'''
            provide the 2 filename IDs to compare, separated by space. 
            BEFORE first, AFTER second. i.e [..] -C -f 1582386835 1582387929'''
            file_name = args.file
    else:
        file_name = None

    returned_dict.update(
        inventory=inventory,
        node=args.node,
        test=args.test,
        before=args.before,
        after=args.after,
        compare=args.compare,
        file_name=file_name
        )

    return returned_dict


class WriteFile():
    def __init__(self, test, node, file_name=None):

        self.test = test
        self.node = node
        self.file_name = file_name
        self.pwd_before = os.getcwd() + '/before/{}'.format(self.test)
        self.pwd_after = os.getcwd() + '/after/{}'.format(self.test)
        self.pwd_diff = os.getcwd() + '/diff/{}'.format(self.test)
        self.time_file = round(time.time())

    def write_before(self, result):
        if not os.path.exists(self.pwd_before) :
            os.makedirs(self.pwd_before)

        with open('{0}/{1}_{2}_{3}.json'.format(
            self.pwd_before, 
            self.time_file,
            self.test, 
            self.node
            ), 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=4)
            print('BEFORE file ID: {}'.format(self.time_file))


    def write_after(self, result):
        if not os.path.exists(self.pwd_after):
            os.makedirs(self.pwd_after)

        with open('{0}/{1}_{2}_{3}.json'.format(
            self.pwd_after,
            self.time_file, 
            self.test, 
            self.node
            ), 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=4)
            print('AFTER file ID: {}'.format(self.time_file))


    def write_diff(self):

        if not os.path.exists(self.pwd_diff) :
            os.makedirs(self.pwd_diff)  
        
        def replace(string, substitutions):

            substrings = sorted(substitutions, key=len, reverse=True)
            regex = re.compile('|'.join(map(re.escape, substrings)))
            
            sub_applied = regex.sub(lambda match: substitutions[match.group(0)], string)
            
            for x in re.findall('\d+:',sub_applied):
                sub_applied = sub_applied.replace(x, f'"{x[:-1]}":')

            return sub_applied

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
            before = open('{0}/{1}_{2}_{3}.json'.format(
                self.pwd_before,
                self.file_name[0],  
                self.test, 
                self.node
                ), 'r')
        except FileNotFoundError as error:
            print(error)
            sys.exit(1)
        
        try:
            after = open('{0}/{1}_{2}_{3}.json'.format(
                self.pwd_after,
                self.file_name[1],  
                self.test,
                self.node), 'r')
        except FileNotFoundError as error:
            print(error)        
            sys.exit(1)
        
        json_diff = str(diff(before, after, load=True, syntax='symmetric'))
        edit_json_diff = replace(json_diff, substitutions)
        diff_file_id = str((self.file_name[0] - self.file_name[1]) * -1)

        with open('{0}/{1}_{2}_{3}.json'.format(
            self.pwd_diff,
            diff_file_id,
            self.test,
            self.node), 'w', encoding='utf-8') as file:
            json.dump(json.loads(edit_json_diff), file, ensure_ascii=False, indent=4)
            print('DIFF file ID: {}'.format(diff_file_id))


def bef_aft_com(node, test, before=None, after=None, compare=None, file_name=None):

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
            wr_diff = WriteFile(test, node, file_name)
            wr_diff.write_diff()


def main():

    my_flags = flags(arguments())

    inventory = my_flags.get('inventory')
    nodes = my_flags.get('node')    
    test = my_flags.get('test')
    before = my_flags.get('before')
    after = my_flags.get('after')
    compare = my_flags.get('compare')
    file_name = my_flags.get('file_name')

    load_config(inventory)
    
    if test:
        for node in nodes:
            bef_aft_com(node, test, before, after, compare, file_name)


if __name__ == '__main__':
    main()
