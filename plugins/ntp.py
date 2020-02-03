#!/usr/bin/env python3
class Ntp():

    def __init__(self, node):
        self.node = node

    @property
    def associations(self):
        return_list = list()

        cmd = self.node.enable('show ntp associations')
        result = cmd[0]['result']

        for values in result.values():
            for peers,attributes in values.items():
                return_list.append("peers: {0}\n".format(peers))
                return_list.append("peerIpAddr: {0}\n".format(attributes.get('peerIpAddr')))
                return_list.append("stratumLevel: {0}\n".format(str(attributes.get('stratumLevel'))))
                return_list.append("reachabilityHistory: {0}\n".format(str(attributes.get('reachabilityHistory')[0])))
        return return_list
