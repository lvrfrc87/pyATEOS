#!/usr/bin/env python3
class mlag():

    def __init__(self, node):
        self.node = node

    @property
    def show(self):

        cmd = self.node.enable('show mlag')
        result = cmd[0]['result']

        return result
