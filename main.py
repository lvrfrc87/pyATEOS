#!/usr/bin/env python3
import os
import re
import sys
import time
import json
import argparse
import threading
from jsondiff import diff
from pprint import pprint
from pyeapi import load_config
from pyeapi import connect_to
from plugins.ntp import Ntp
from plugins.snmp import Snmp

def arguments():
    # Add mutually exclusive
    # parser.add_argument('--routing', dest='routing', action='store_true', help="run only Routing Protocol test")
    # parser.add_argument('--iface', dest='iface', action='store_true', help="run only Interface test")
    parser = argparse.ArgumentParser(
        description="pyATEOS - A simple python application for operational status test on Arista device."
        )

    parser.add_argument(
        '--inventory',
        dest='inventory',
        help="inventory file"
        )

    parser.add_argument(
        '--node',
        dest='node',
        help="specify inventory node",
        nargs='+',
        required=True
        )

    parser.add_argument(
        '--before',
        dest='before',
        action='store_true',
        help="json file containing the test result BEFORE the conifg-change"
        )

    parser.add_argument(
        '--after',
        dest='after',
        action='store_true',
        help="json file containing the test result AFTER the conifg-change"
        )

    parser.add_argument(
        '--test',
        dest='test',
        help="run a specific test"
        )

    parser.add_argument(
        '--mgmt',
        dest='mgmt',
        action='store_true',
        help="run only Management test"
        )

    parser.add_argument(
        '--all',
        dest='all',
        action='store_true',
        help="run All kind of test"
        )

    parser.add_argument(
        '--compare',
        dest='compare',
        action='store_true',
        help="compare before vs. after"
        )

    return parser.parse_args()


def flags(args):

    returned_dict = dict()

    # if args.before:
    #     folder = 'before'
    #     file_name = round(time.time())
    # elif args.after:
    #     folder = 'after'
    #     file_name = round(time.time())

    if args.inventory:
        inventory = args.inventory
    else:
        inventory = 'eos_inventory.ini'

    returned_dict.update(
        inventory=inventory,
        node=args.node,
        mgmt=args.mgmt,
        all=args.all,
        test=args.test,
        before=args.before,
        after=args.after,
        compare=args.compare
        )

    return returned_dict


# def filesystem_build():
#     folders_test = [
#         'ntp'
#     ]

#     if not os.path.exists(self.pwd_before):
#         os.makedirs(self.pwd_before)

#     if not os.path.exists(self.pwd_after):
#         os.makedirs(self.pwd_after)

#     for test in folders_test:
#         if not os.path.exists(self.pwd_before + '/' + test) :
#             os.makedirs(self.pwd_before + '/' + test)

#         if not os.path.exists(self.pwd_after + '/' + test) :
#             os.makedirs(self.pwd_after + '/' + test)

#         if not os.path.exists(self.pwd_diff + '/' + test) :
#             os.makedirs(self.pwd_diff + '/' + test)


class WriteFile():
    def __init__(self, test, node):
        self.test = test
        self.node = node
        self.pwd_before = os.getcwd() + '/' + 'before'
        self.pwd_after = os.getcwd() + '/' + 'after'
        self.pwd_diff = os.getcwd() + '/' + 'diff'
        folders_test = [
        'ntp',
        'snmp'
        ]

        if not os.path.exists(self.pwd_before):
            os.makedirs(self.pwd_before)

        if not os.path.exists(self.pwd_after):
            os.makedirs(self.pwd_after)

        for test in folders_test:
            if not os.path.exists(self.pwd_before + '/' + test) :
                os.makedirs(self.pwd_before + '/' + test)

            if not os.path.exists(self.pwd_after + '/' + test) :
                os.makedirs(self.pwd_after + '/' + test)

            if not os.path.exists(self.pwd_diff + '/' + test) :
                os.makedirs(self.pwd_diff + '/' + test)  
    
    def write_before(self, result):
        with open('{}/{}/{}_{}.json'.format(self.pwd_before, self.test, self.test, self.node), 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=4)


    def write_after(self, result):
        with open('{}/{}/{}_{}.json'.format(self.pwd_after, self.test, self.test, self.node), 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=4)


    def write_diff(self):
        
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
            ')':']'
            }

        before = open('{}/{}/{}_{}.json'.format(self.pwd_before, self.test, self.test, self.node), 'r')
        after = open('{}/{}/{}_{}.json'.format(self.pwd_after, self.test, self.test, self.node), 'r')
        
        json_diff = str(diff(before, after, load=True, syntax='symmetric'))
        edit_json_diff = replace(json_diff, substitutions)
        final_diff = json.loads(edit_json_diff)

        with open('{}/{}/{}_{}.json'.format(self.pwd_diff, self.test, self.test, self.node), 'w', encoding='utf-8') as file:
            json.dump(final_diff, file, ensure_ascii=False, indent=4)


def main():

    my_flags = flags(arguments())

    inventory = my_flags.get('inventory')
    node = my_flags.get('node')[0]
    mgmt = my_flags.get('mgmt')
    all = my_flags.get('all')
    test = my_flags.get('test')
    before = my_flags.get('before')
    after = my_flags.get('after')
    compare = my_flags.get('compare')

    load_inventory = load_config(inventory)
    connect_node = connect_to(node)

    if test:
        if test == 'ntp':
            if before:
                wr_before = WriteFile('ntp', node)
                wr_before.write_before(Ntp(connect_node).associations)
                # write_before('ntp', node, Ntp(connect_node).associations)

            if after:
                # write_after('ntp', node, Ntp(connect_node).associations)
                wr_after = WriteFile('ntp', node)
                wr_after.write_after(Ntp(connect_node).associations)

            if compare:
                wr_diff = WriteFile('ntp', node)
                wr_diff.write_diff()


if __name__ == '__main__':
    main()
