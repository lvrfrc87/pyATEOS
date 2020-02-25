#!/usr/bin/env python3
from pyeapi import eapilib

class vxlan():

    def __init__(self, node):
        self.node = node

    @property
    def show(self):

        try:
            cmd = self.node.enable('show interfaces vxlan 1')
            result = cmd[0]['result']

            return result

        except eapilib.CommandError:
            print('VXLAN command "show interfaces vxlan 1" not support by the platform')
       

