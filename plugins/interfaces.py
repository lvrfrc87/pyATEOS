#!/usr/bin/env python3
class Interfaces():

    def __init__(self, node):
        self.node = node

    @property
    def show(self):
        return_list = list()

        cmd = self.node.enable('show interfaces')
        result = cmd[0]['result']

        for attributes in result['interfaces'].values():
            return_list.append("name: {0}\n".format(attributes.get('name')))
            return_list.append("interfaceStatus: {0}\n".format(attributes.get('interfaceStatus')))
            return_list.append("autoNegotiate: {0}\n".format(str(attributes.get('autoNegotiate'))))
            return_list.append("mtu: {0}\n".format(str(attributes.get('mtu'))))
            return_list.append("duplex: {0}\n".format(str(attributes.get('duplex'))))
            return_list.append("bandwidth: {0}\n".format(str(attributes.get('bandwidth'))))
            return_list.append("forwardingModel: {0}\n".format(str(attributes.get('forwardingModel'))))
            return_list.append("lineProtocolStatus: {0}\n".format(str(attributes.get('lineProtocolStatus'))))

            for adresses in attributes.get('interfaceAddress'):
                return_list.append("maskLen: {0}\n".format(adresses.get('primaryIp').get('maskLen')))
                return_list.append("address: {0}\n".format(adresses.get('primaryIp').get('address')))


        return return_list
