#!/usr/bin/env python3
class vrf():

    def __init__(self, node):
        self.node = node

    @property
    def show(self):

        cmd = self.node.enable('show vrf')
        result = cmd[0]['result']

        return result
