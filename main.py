#!/usr/bin/env python3
import os
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


def filesystem_build():
    folders_test = [
        'ntp'
    ]

    if not os.path.exists(PWD_BEFORE):
        os.makedirs(PWD_BEFORE)

    if not os.path.exists(PWD_AFTER):
        os.makedirs(PWD_AFTER)

    for test in folders_test:
        if not os.path.exists(PWD_BEFORE + '/' + test) :
            os.makedirs(PWD_BEFORE + '/' + test)

        if not os.path.exists(PWD_AFTER + '/' + test) :
            os.makedirs(PWD_AFTER + '/' + test)

        if not os.path.exists(PWD_DIFF + '/' + test) :
            os.makedirs(PWD_DIFF + '/' + test)

def test_ntp(node):
    print('Run NTP operational test')
    ntp = Ntp(node).associations

    return ntp


def write_before(test, node, result):
    with open('{}/{}/{}_{}.json'.format(PWD_BEFORE,test, test, node), 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)


def write_after(test, node, result):
    with open('{}/{}/{}_{}.json'.format(PWD_AFTER,test, test, node), 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)


def test_ntp(connect_node):
    print("Run operational test for NTP servers")
    ntp = Ntp(connect_node).associations

    return ntp


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
                write_before('ntp', node, test_ntp(connect_node))
            if after:
                write_before('ntp', node, test_ntp(connect_node))



    if compare:
        before = open('{}/ntp/ntp_{}.json'.format(PWD_BEFORE, node), 'r')
        after = open('{}/ntp/ntp_{}.json'.format(PWD_AFTER, node), 'r')
        json_diff = str(diff(before, after, load=True, syntax='symmetric'))
        edit_json_diff = json_diff.replace('\'', '\"').replace('insert','"insert"').replace('delete','"delete"').replace('[','"[').replace(']', ']"')
        b = json.loads(edit_json_diff)
        print(json.dumps(b, indent=4))

        with open('{}/ntp/ntp_{}.json'.format(PWD_DIFF, node), 'w', encoding='utf-8') as file:
            json.dump(b, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    PWD_BEFORE = os.getcwd() + '/' + 'before'
    PWD_AFTER = os.getcwd() + '/' + 'after'
    PWD_DIFF = os.getcwd() + '/' + 'diff'

    filesystem_build()
    main()
