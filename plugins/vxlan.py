#!/usr/bin/env python3
class vxlan():

    def __init__(self, node):
        self.node = node

    @property
    def show(self):

        cmd = self.node.enable('show interface vxlan 1')
        result = cmd[0]['result']

        return result
