#!/usr/bin/env python3
class Acl():

    def __init__(self, node):
        self.node = node

    @property
    def show(self):

        cmd = self.node.enable('show ip acl')
        result = cmd[0]['result']

        return result
