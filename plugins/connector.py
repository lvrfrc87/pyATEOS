import os
import sys
import yaml
import platform

CONFIG_SEARCH_PATH  = ['.eos_inventory.yaml', '.eos_inventory.yml']

class Inventory():

    def __init__(self,filename=None):
        self.filename = filename

    @property
    def load_inventory(self):

        path = list(CONFIG_SEARCH_PATH)

        if 'EOS_INVENTORY' in os.environ:
            path = list(os.environ['EOS_INVENTORY'])
        elif self.filename:
            path = list(self.filename)

        for inv in path:
            try:
                inventory = yaml.safe_load(open(os.path.abspath(inv), 'rb'))
            except IOError:
                continue

        try:
            return inventory
        except UnboundLocalError:
            print('''Please provide one of the following:
                1 - inventory file path as argument
                2 - EOS_INVENTORY ENV variable containing file paths
                3 - inventory under ".eos_inventory.yaml" or ".eos_inventory.yml" ''')
            sys.exit(1)


inv = Inventory()

print(inv.load_inventory)
