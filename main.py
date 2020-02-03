#!/usr/bin/env python3
import sys
import time
import difflib
from pyeapi import load_config
from pyeapi import connect_to
from pyeapi import connect_to
from plugins.ntp import Ntp
from plugins.snmp import Snmp
from plugins.interfaces import Interfaces
from colorama import Fore, Back, Style, init

load_config('eos_inventory.ini')
node = connect_to('localhost')

ntp = Ntp(node).associations
snmp = Snmp(node).host
iface = Interfaces(node).show

final_list = ntp + snmp + iface
file = open('{}.txt'.format(sys.argv[1]),'w')
for i in final_list:
    file.write(str(i))
file.close()

text1 = open("before.txt").readlines()
text2 = open("after.txt").readlines()

diff = difflib.unified_diff(
    text1,
    text2,
    fromfile='before.txt',
    tofile='after.txt',
    lineterm='',
    n=0)

for line in diff:
    if line.startswith('+'):
        print(Fore.GREEN + line.strip('\n') + Fore.RESET)
    elif line.startswith('-'):
        print(Fore.RED + line.strip('\n') + Fore.RESET)
    elif line.startswith('^'):
        print(Fore.BLUE + line.strip('\n') + Fore.RESET)
    else:
        print(line.strip('\n'))
