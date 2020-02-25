#!/usr/bin/env python3
class snmp():

    def __init__(self, node):
        self.node = node

    @property
    def show(self):

        cmd = self.node.enable('show snmp host')
        result = cmd[0]['result']

        return result