#!/usr/bin/env python3
class stp():

    def __init__(self, node):
        self.node = node

    @property
    def show(self):

        cmd = self.node.enable('show spanning-tree topology status')
        result = cmd[0]['result']

        return result
