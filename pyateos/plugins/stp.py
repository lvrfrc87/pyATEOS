#!/usr/bin/env python3
class stp():

    def __init__(self, node):
        self.node = node

    @property
    def show(self):

        cmd = self.node.enable('show spanning-tree topology status')
        result = cmd[0]['result']

        return result
<<<<<<< HEAD
=======

>>>>>>> 5c411facf0c54cd55cba37c26f939847f3ae3b43
