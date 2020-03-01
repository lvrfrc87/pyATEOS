#!/usr/bin/env python3
class lldp():

    def __init__(self, node):
        self.node = node

    @property
    def show(self):

        cmd = self.node.enable('show lldp neighbors')
        result = cmd[0]['result']

        return result
