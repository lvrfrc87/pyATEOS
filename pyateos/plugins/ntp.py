#!/usr/bin/env python3
class ntp():
    def __init__(self, node):
        self.node = node

    @property
    def show(self):

        cmd = self.node.enable('show ntp associations')
        result = cmd[0]['result']

        return result
