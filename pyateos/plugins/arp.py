#!/usr/bin/env python3
class arp():

    def __init__(self, node):
        self.node = node

    @property
    def show(self):

        cmd = self.node.enable('show ip arp')
        result = cmd[0]['result']

        return result

#f20200301