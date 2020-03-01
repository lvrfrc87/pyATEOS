#!/usr/bin/env python3
class mac():

    def __init__(self, node):
        self.node = node

    @property
    def show(self):

        cmd = self.node.enable('how mac address-table')
        result = cmd[0]['result']

        return result

#f20200301