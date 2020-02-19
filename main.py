#!/usr/bin/env python3
import os
import sys
import time
import argparse
import threading
from jsondiff import diff
from pyeapi import load_config
from pyeapi import connect_to
from plugins import *

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
        '--mgmt',
        dest='mgmt',
        action='store_true',
        help="run only Management test"
        )

    parser.add_argument(
        '--all',
        dest='all',
        action='store_false',
        help="run All kind of test"
        )

    return parser.parse_args()


def flags(args):

    returned_dict = dict()

    if args.before:
        folder = 'before'
        file_name = round(time.time())
    elif args.after:
        folder = 'after'
        file_name = round(time.time())

    if args.inventory:
        inventory = args.inventory
    else:
        inventory = 'eos_inventory.ini'

    returned_dict.update(
        folder=folder,
        file_name=file_name,
        inventory=inventory,
        node=args.node,
        mgmt=args.mgmt,
        all=args.all
        )

    return returned_dict


# def thread_cmd():
#     cmd_threads = list()
#     az = os.environ['AZ']
#     for region, target_list in dic_targets.items():
#         if region == az:
#             for target in target_list:
#                 thread_targets = threading.Thread(target=influxdb_call, args=(target, region))
#                 thread_targets.start()
#                 ping_threads.append(thread_targets)
#         else:
#             pass

def test_list(flag, node):

    my_test_list = list()

    if flag == 'mgmt':
        ntp_test = ntp.Ntp(node).associations
        snmp_test = snmp.Snmp(node).host

        return ntp, snmp

    elif flag == 'all':
        ntp = ntp.Ntp(node).associations
        snmp = snmp.Snmp(node).host
        iface = iface.Interfaces(node).show
        stp = stp.Stp(node).topology
        vlans = vlans.Vlans(node).show
        vrfs = vrfs.Vrfs(node).show
        vxlan = vxlan.Vxlan(node).vni
        acls = acls.Acl(node).show
        prefix_lists = prefix_lists.PrefixList(node).show
        route_maps = route_maps.RouteMap(node).show
        as_path =route_maps. AsPath(node).show
        mlag = mlag.Mlag(node).show
        ip_route = ip_route.IpRoute(node).show
        bgp_ipv4 = bgp_ipv4.BgpIpv4(node).show
        bgp_evpn = bgp_evpn.BgpEvpn(node).show



def main():

    my_flags = flags(arguments())

    inventory = load_config(my_flags.get('inventory'))
    node = connect_to(my_flags.get('node')[0])
    folder_path =  os.getcwd() + '/' + my_flags.get('folder')

    if my_flags.get('mgmt'):
        flag = 'mgmt'
    elif my_flags.get('all'):
        flag = 'all'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    print(ntp.Ntp(node).associations)


    print(test_list(flag, node))



    # TO DO - mutlithreading

    # # final_list = ntp + snmp + iface
    # final_list = ntp
    #
    # file = open('{}.txt'.format(sys.argv[1]),'w')
    #
    # for i in final_list:
    #     file.write(str(i))
    # file.close()
    #
    # text1 = open("before.txt").readlines()
    # text2 = open("after.txt").readlines()


if __name__ == '__main__':
    main()
