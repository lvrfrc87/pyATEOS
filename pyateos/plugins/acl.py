#!/usr/bin/env python3
class acl():

    def __init__(self, node):
        self.node = node

    @property
    def show(self):

        cmd = self.node.enable('show ip access-lists')
        result = cmd[0]['result']

        return result
