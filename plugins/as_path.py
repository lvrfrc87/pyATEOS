#!/usr/bin/env python3
class as_path():

    def __init__(self, node):
        self.node = node

    @property
    def show(self):

        cmd = self.node.enable('show ip as-path')
        result = cmd[0]['result']

        return result
