#!/usr/bin/env python3
from pyeapi import eapilib

class bgp_ipv4():

    def __init__(self, node):
        self.node = node

    @property
    def show(self):

        try:
            cmd = self.node.enable('show bgp ipv4 unicast')
            result = cmd[0]['result']

            return result

        except eapilib.CommandError:
            print('BGP IPv4 command "show bgp ipv4 unicast" not support by the platform')
