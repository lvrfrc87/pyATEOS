#!/usr/bin/env python3
import sys
import time
import difflib
from pyeapi import load_config
from pyeapi import connect_to
from pyeapi import connect_to
from plugins.ntp import Ntp
from colorama import Fore, Back, Style, init

load_config('eos_inventory.ini')
node = connect_to('localhost')

filename = sys.argv[1]
ntp = Ntp(node).associations
file = open('ntp_{}.json'.format(filename),'w')
for i in ntp:
    file.write(str(i))
file.close()

text1 = open("ntp_yesterday.json").readlines()
text2 = open("ntp_today.json").readlines()

diff = difflib.unified_diff(
    text1,
    text2,
    fromfile='ntp_yesterday.json',
    tofile='ntp_today.json',
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
