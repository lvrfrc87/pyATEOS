#!/usr/bin/env python3
class route_map():

    def __init__(self, node):
        self.node = node

    @property
    def show(self):

        cmd = self.node.enable('show route-map')
        result = cmd[0]['result']

        return result
