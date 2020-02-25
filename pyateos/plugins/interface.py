#!/usr/bin/env python3
class interface():

    def __init__(self, node):
        self.node = node

    @property
    def show(self):

        cmd = self.node.enable('show interfaces')
        result = cmd[0]['result']

        return result
