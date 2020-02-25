#!/usr/bin/env python3
class prefix_list():

    def __init__(self, node):
        self.node = node

    @property
    def show(self):

        cmd = self.node.enable('show ip prefix-list')
        result = cmd[0]['result']

        return result
