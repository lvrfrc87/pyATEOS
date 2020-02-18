#!/usr/bin/env python3
class Stp():

    def __init__(self, node):
        self.node = node

    @property
    def topology(self):

        cmd = self.node.enable('show spanning-tree topology status')
        result = cmd[0]['result']

        return result

        # for values in result.values():
        #     for peers,attributes in values.items():
        #         return_list.append("peers: {0}\n".format(peers))
        #         return_list.append("peerIpAddr: {0}\n".format(attributes.get('peerIpAddr')))
        #         return_list.append("stratumLevel: {0}\n".format(str(attributes.get('stratumLevel'))))
        #         return_list.append("reachabilityHistory: {0}\n".format(str(attributes.get('reachabilityHistory')[0])))
        # return return_list
