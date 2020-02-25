#!/usr/bin/env python3
from pyeapi import eapilib

class bgp_evpn():

    def __init__(self, node):
        self.node = node

    @property
    def show(self):

        try:
            cmd = self.node.enable('show bgp evpn')
            result = cmd[0]['result']

            return result

        except eapilib.CommandError:
            print('BGP EVPN command "show bgp evpn" not support by the platform')
