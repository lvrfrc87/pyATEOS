#!/usr/bin/env python3
import sys
import time
import argparse
from pyeapi import load_config
from pyeapi import connect_to
# from plugins.acl import Acl
# from plugins.as_path import AsPath
# from plugins.bgp_evpn import BgpEvpn
# from plugins.bgp_ipv4 import BgpIpv4
# from plugins.interfaces import Interfaces
# from plugins.ip_routes import IpRoutes
# from plugins.mlag import Mlag
# from plugins.ntp import Ntp
# from plugins.prefix_lists import PrefixLists
# from plugins.route_maps import RouteMaps
# from plugins.snmp import Snmp
# from plugins.stp import Stp
# from plugins.vlans import Vlans
# from plugins.vrfs import Vrfs
# from plugins.vxlans import Vxlans
from plugins import *
# from colorama import Fore, Back, Style, init


def main():

    # Add mutually exclusive
    # parser = argparse.ArgumentParser(description="pyATEOS - A simple python application for operational status test on Arista device.")
    # parser.add_argument('--before', dest='before', help="json file containing the test result BEFORE the conifg-change",type=str)
    # parser.add_argument('--after', dest='after', help="json file containing the test result AFTER the conifg-change", type= str)
    # parser.add_argument('--mgmt', dest='mgmt', action='store_true',help="run only Management test")
    # parser.add_argument('--routing', dest='routing', action='store_true', help="run only Routing Protocol test")
    # parser.add_argument('--iface', dest='iface', action='store_true', help="run only Interface test")
    # parser.add_argument('--all', dest='all', action='store_false', help="run All kind of test")
    # parser.add_argument('--inventory', dest='inventory', help="inventory file")
    #
    # args = parser.parse_args()
    #
    # before = args.before
    # after = args.after
    # mgmt = args.mgmt
    # routing = args.routing
    # iface = args.iface
    # all = args.all
    #
    # if args.inventory:
    #     inventory = load_config(args.inventory)
    # else:
    #     inventory = load_config('eos_inventory.ini')

    inventory = load_config('eos_inventory.ini')
    node = connect_to('svc1a')

    print(ntp.Ntp(node).associations)

    # print(plugins.ntp.Ntp(node).associations)


    # TO DO - mutlithreading
    # ntp = Ntp(node).associations
    # snmp = Snmp(node).host
    # iface = Interfaces(node).show
    # stp = Stp(node).topology
    # vlans = Vlans(node).show
    # vrfs = Vrfs(node).show
    # vxlan = Vxlan(node).vni
    # acls = Acl(node).show
    # prefix_lists = PrefixList(node).show
    # route_maps = RouteMap(node).show
    # as_path = AsPath(node).show
    # mlag = Mlag(node).show
    # ip_route = IpRoute(node).show
    # bgp_ipv4 = BgpIpv4(node).show
    # bgp_evpn = BgpEvpn(node).show
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

# diff = difflib.unified_diff(
#     text1,
#     text2,
#     fromfile='before.txt',
#     tofile='after.txt',
#     lineterm='',
#     n=0)
#
# for line in diff:
#     if line.startswith('+'):
#         print(Fore.GREEN + line.strip('\n') + Fore.RESET)
#     elif line.startswith('-'):
#         print(Fore.RED + line.strip('\n') + Fore.RESET)
#     elif line.startswith('^'):
#         print(Fore.BLUE + line.strip('\n') + Fore.RESET)
#     else:
#         print(line.strip('\n'))

if __name__ == '__main__':
    main()
