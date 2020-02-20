#!/usr/bin/env python3
class ip_route():

    def __init__(self, node):
        self.node = node

    @property
    def show(self):

        cmd = self.node.enable('show ip route detail')
        result = cmd[0]['result']

        return result
