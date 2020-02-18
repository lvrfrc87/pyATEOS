#!/usr/bin/env python3
class BgpIpv4():

    def __init__(self, node):
        self.node = node

    @property
    def show(self):

        cmd = self.node.enable('show bgp ipv4 unicast')
        result = cmd[0]['result']

        return result
