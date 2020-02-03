#!/usr/bin/env python3
class Snmp():

    def __init__(self, node):
        self.node = node

    @property
    def host(self):
        return_list = list()

        cmd = self.node.enable('show snmp host')
        result = cmd[0]['result']

        # TO DO - SNMPv3
        for values in result.values():
            for attributes in values:
                return_list.append("communityString: {0}\n".format(attributes.get('v1v2cParams').get('communityString')))
                return_list.append("vrf: {0}\n".format(attributes.get('vrf')))
                return_list.append("protocolVersion: {0}\n".format(attributes.get('protocolVersion')))
                return_list.append("hostname: {0}\n".format(attributes.get('hostname')))
                return_list.append("notificationType: {0}\n".format(attributes.get('notificationType')))
                return_list.append("port: {0}\n".format(attributes.get('port')))
        return return_list
