#!/usr/bin/env python3
class Vxlans():

    def __init__(self, node):
        self.node = node

    @property
    def vni(self):

        cmd = self.node.enable('show interface vxlan 1')
        result = cmd[0]['result']

        return result
