# pyATEOS

Deliberately inspired by [pyATS](https://developer.cisco.com/docs/pyats/) and based on [pyEAPI](https://pyeapi.readthedocs.io/en/latest/), [jsodiff](https://github.com/fzumstein/jsondiff) and [jmespath](http://jmespath.org/) libraries, pyATEOS is a python framework for operational status tests on Arista network gear. pyATS is based on SSH show command parsed via regex. Thanks to the powerful Arista API, every show command can be returned in JSON format skipping all the parse unstructured output pain. Ideally, a day pyATS will supprt Arista API as well.

## TABLE OF CONTENT
----
- HOW IT WORKS
- HOW TO RUN - API
- HOW TO RUN - CLI
- FILTER
- TEST SUPPORTED
- THE `SHOW` COMMANDS BEHIND THE PLUGINS
- ANSIBLE PYATEOS
----

### HOW IT WORKS
A snapshot of the operational status of a switch is taken before a config or network change and compare against a second snapshot taken after the change. A diff file is generated in .json format.

Diff example after removing a NTP server and add new one:

```
{
    "peers": {
[...]
        "insert": {
            "216.239.35.0": {
                "delay": 10.11,
                "jitter": 0.0,
                "lastReceived": 1582533810.0,
                "peerType": "unicast",
                "reachabilityHistory": [
                    true
                ],
                "condition": "reject",
                "offset": 160338.608,
                "peerIpAddr": "216.239.35.0",
                "pollInterval": 64,
                "refid": ".GOOG.",
                "stratumLevel": 1
            }
        },
        "delete": {
            "10.75.33.5": {
                "delay": 0.0,
                "jitter": 0.0,
                "lastReceived": 2085978496.0,
                "peerType": "unicast",
                "reachabilityHistory": [
                    false
                ],
                "condition": "reject",
                "offset": 0.0,
                "peerIpAddr": "10.75.33.5",
                "pollInterval": 1024,
                "refid": ".INIT.",
                "stratumLevel": 16
            }
        }
    }
}
```

Remember, this does not show a config change, instead it shows the difference of the operational status of the NTP servers. This means that you will see a diff in `jitter` or `offset` between 2 snapshots. Example:

```
{
    "peers": {
        "ns2.sys.cloudsys.tmcs": {
            "jitter": [
                6.36,
                3.826
            ],
            "lastReceived": [
                1582537393.0,
                1582537586.0
            ],
            "condition": [
                "candidate",
                "sys.peer"
            ]
        },
        "ns1.sys.cloudsys.tmcs": {
            "delay": [
                0.408,
                0.355
            ],
            "jitter": [
                5.075,
                6.241
            ],
            "lastReceived": [
                1582537405.0,
                1582537605.0
            ],
            "condition": [
                "sys.peer",
                "candidate"
            ],
            "offset": [
                5.477,
                -6.42
            ]
        }
    }
}
```
### HOW TO RUN - API
```
>>> from pyateos import pyateos
>>> 
>>> my_dict = {
    'invetory': 'eos_invenotry.ini',
    'before': True,
    'after': False,
    'compare': False,
    'test': ['ntp'],
    'node': ['lf4'],
    'file_name': None,
    'filter': False
}
>>> 
>>> pyateos.pyateos(**my_dict)
>>> BEFORE file ID for NTP test: 1582619302
>>> 
>>> my_dict = {
    'invetory': 'eos_invenotry.ini',
    'before': False,
    'after': True,
    'compare': False,
    'test': ['ntp'],
    'node': ['lf4'],
    'file_name': None,
    'filter': False
}
>>> 
>>> pyateos.pyateos(**my_dict)
>>> AFTER file ID for NTP test: 1582619366
>>> 
>>> my_dict = {
    'invetory': 'eos_invenotry.ini',
    'before': False,
    'after': False,
    'compare': True,
    'test': ['ntp'],
    'node': ['lf4'],
    'file_name': [1582619302, 1582619366]
    'filter': False,
}
>>> 
>>> pyateos.pyateos(**my_dict)
>>> DIFF file ID for NTP test: 64
```

### HOW TO RUN - CLI
An inventory must be defined as described in pyEAPI [doc](https://pyeapi.readthedocs.io/en/latest/configfile.html). A filesystem is automatically created at every code iteration (if required - idempotent). The fiename of before and after are in the follwing format `timestamp_node_test.json`. Diff filename is `(after_timpestamp - before_timestamp)_node_test.json`.

Arguments list:

```
    usage: pyATEOS [-h] (-B | -A | -C) -t TEST [TEST ...] [-g GROUP [GROUP ...]]
               [-i INVENTORY] -n NODE [NODE ...] [-F FILE [FILE ...]] [-f]

    pyATEOS - A simple python application for operational status test on Arista
    device. Based on pyATS idea and pyeapi library for API calls.

    optional arguments:
    -h, --help            show this help message and exit
    -B, --before          write json file containing the test result BEFORE. To
                            be run BEFORE the config change. File path example:
                            $PWD/before/ntp/router1_ntp.json
    -A, --after           write json file containing the test result AFTER. To
                            be run AFTER the config change. File path example:
                            $PWD/after/ip_route/router1_ip_route.json
    -C, --compare         diff between before and after test files. File path
                            example: $PWD/diff/snmp/router1_snmp.json
    -t TEST [TEST ...], --test TEST [TEST ...]
                            run one or more specific test. Multiple values are
                            accepted separated by space
    -g GROUP [GROUP ...], --group GROUP [GROUP ...]
                            run a subset of test. Options available: mgmt,
                            routing, layer2, ctrl, all Multiple values are
                            accepted separated by space. Works also with -t --test
    -i INVENTORY, --inventory INVENTORY
                            specify pyeapi inventory file path
    -n NODE [NODE ...], --node NODE [NODE ...]
                            specify inventory node. Multiple values are accepted
                            separated by space
    -F FILE [FILE ...], --file_name FILE [FILE ...]
                            provide the 2 filename IDs to compare, separated by
                            space. BEFORE first, AFTER second. i.e [..] -C -f
                            1582386835 1582387929
    -f, --filter          filter counters where present
```
 
example - BEFORE a network config change for NTP server:

```
pyateos -i eos_inventory.ini -n lf4 -t mgmt -B
BEFORE file ID for NTP test: 1582537406
BEFORE file ID for SNMP test: 1582537409

ls -la before/ntp/
-rw-r--r--  1 federicoolivieri  staff   916 24 Feb 09:47 1582537406.json
```

example - AFTER a network config change for NTP server:

```
pyateos -i eos_inventory.ini -n lf4 -t mgmt -A
AFTER file ID for NTP test: 1582537612
AFTER file ID for SNMP test: 1582537614

ls -la after/ntp/
-rw-r--r--  1 federicoolivieri  staff  1246 24 Feb 10:43 1582537612.json
```

diff example of the aboves for NTP.

```
pyateos -i eos_inventory.ini -n lf4 -t ntp -C -F 1582537612 1582537406
DIFF file ID for NTP test: 6

ls -la diff/ntp/
-rw-r--r--  1 federicoolivieri  staff     2 24 Feb 10:43 6_ntp_lf4.json
```

`group` and `test` can be use together:

```
pyateos -g mgmt -t bgp_evpn -n lf4 -i ../eos_inventory.ini -B
BEFORE file ID for NTP test: 1583161168
BEFORE file ID for BGP_EVPN test: 1583161171
BEFORE file ID for SNMP test: 1583161172
```

Even thugh `before` and `after` test can be run using groups, every diff must be run for every single test. Is not possible (yet) to run diff for a group of test

### FILTER
Some test outputs like interfaces or ntp have counters that constantly change. Therefore the diff will aways return a quite verbose output, making difficult to spot the what has been `insert` or `delete`. Apply `-f` or `--filter` will prune all unecessary counters.
Filters are only valid for those test that return dict(dict()). For dict(list()) return, filters are transparent.

Example no filter applied to NTP test

```
pyateos -n lf4 -t ntp -C -F 1582732433 1582732569

{
    "peers": {
        "ns1.sys.cloudsys.tmcs": {
            "delay": [
                0.441,
                0.505
            ],
            "jitter": [
                0.49,
                0.004
            ],
            "lastReceived": [
                1582732381.0,
                1582732522.0
            ],
            "reachabilityHistory": {
                "delete":
            [...]
        },
        "delete": {
            "ns2.sys.cloudsys.tmcs": {
                "delay": 0.441,
                "jitter": 0.457,
                "lastReceived": 1582732328.0,
                "peerType": "unicast",
                "reachabilityHistory": [
                    true,
                    true,
                    true,
                    true,
                    true,
                    true,
                    true,
                    true
                ],
                "condition": "candidate",
                "offset": -0.509,
                "peerIpAddr": "10.75.33.5",
                "pollInterval": 1024,
                "refid": "169.254.0.1",
                "stratumLevel": 3
            }
        }
    }
}
```

Example with filter applied to the same test above.

```
pyateos -n lf4 -t ntp -C -F 1582732433 1582732569 -f

{
    "delete": {
        "ns2.sys.cloudsys.tmcs": {
            "delay": 0.441,
            "jitter": 0.457,
            "lastReceived": 1582732328.0,
            "peerType": "unicast",
            "reachabilityHistory": [
                true,
                true,
                true,
                true,
                true,
                true,
                true,
                true
            ],
            "condition": "candidate",
            "offset": -0.509,
            "peerIpAddr": "10.75.33.5",
            "pollInterval": 1024,
            "refid": "169.254.0.1",
            "stratumLevel": 3
        }
    },
    "insert": null
}
```

### TEST SUPPORTED

All test supported are available under `plugins` folder. Those are:

```
acl
as_path
bgp_evpn
bgp_ipv4
interface
ip_route
mlag
ntp
prefix_list
route_map
snmp
stp
vlan
vrf
vxlan
```

Some of the test are grouped together like: 

`mgmt: ntp, snmp`, 

`routing: bgp_evpn, bgp_ipv4, ip_route`, 

`layer2: stp, vlan, vxlan, lldp, arp, mac`,

`ctrl: acl, as_path, prefix_list, route_map` 

`all` running all test availables under `plugins`. 

### ADD NEW PLUGINS
New plugins can be easily created and added under `plugins/` folder. Give to the file a meaningful name and copy the below content. The test name will be equal to the class name.

```
#!/usr/bin/env python3
from pyeapi import eapilib

class my_test():

    def __init__(self, node):
        self.node = node

    @property
    def show(self):

        try:
            cmd = self.node.enable('show my command')
            result = cmd[0]['result']

            return result

        except eapilib.CommandError:
            print('COMMAND command "show my command not support by the platform')
```

Look for `test_all` list and add your test there. If you want, you can add your test to an existing group or create your own group:

```
    test_all = [
        'my_test'
        [..]
        'vrf',
        'vxlan'
    ]
```

### THE `SHOW` COMMANDS COMMANDS BEHIND THE PLUGINS
Every pyATEOS plugin run a specific run command. To better understand which output you will expect by each test, here the full list of plugins/commands:
```
acl:            show ip access-lists
arp:            show ip arp
as_path:        show ip as-path access-list
bgp_evpn:       show bgp evpn
bgp_ipv4:       show bgp ipv4 unicast
interface:      show interfaces
ip_route:       show ip route detail
lldp:           show lldp neighbors
mac:            show address-table
mlag:           show mlag
ntp:            show ntp associations
prefix_list:    show ip prefix-list
route_map:      show route-map
snmp:           show snmp host
vlan:           show vlan
vrf:            show vrf
vxlan:          show interfaces vxlan 1
```

### ANSIBLE PYATEOS
Good news for Ansible folks, pyATEOS is supported by Ansible. `eos_pyateos` module is available. You can add under your [collection](https://galaxy.ansible.com/docs/contributing/creating_collections.html) or under `ansible/modules/network/eos/eos_pyateos.py`. Examples, test results and modules available under `ansible/`.

Here and example of Ansible playbook using `eos_pyateos`:

```
- name: run BEFORE tests.
  eos_pyateos:
      before: true
      test:
          - acl
      group: 
          - mgmt
          - layer2
      hostname: "{{ inventory_hostname }}"
  register: result

- name: save BEFORE file IDs.
  delegate_to: 127.0.0.1
  set_fact:
      before_ids: "{{ result.before_file_ids }}"

- name: change mgmt config on switch.
  eos_config:
      lines:
          - no ntp server vrf mgmt 10.75.33.5
          - ntp server vrf mgmt 216.239.35.4
          - no snmp-server host 10.1.22.1 vrf mgmt version 2c snmp_pass
          - snmp-server host 10.1.22.9 vrf mgmt version 2c snmp_pass

- name: shutdown interface.
  eos_config:
      lines:
          - shutdown
      parents: interface Ethernet50/1

- name: edit ACL.
  eos_config:
      lines:
          - no 10
          - 10 remark pyATEOS TEST
      parents: ip access-list standard SNMP

- name: run AFTER tests.
  eos_pyateos:
      after: true
      test:
          - acl
      group:
          - mgmt
          - layer2
      hostname: "{{ inventory_hostname }}"
  register: result

- name: save AFTER file IDs.
  delegate_to: 127.0.0.1
      set_fact:
          after_ids: "{{ result.after_file_ids }}"
 
- name: run DIFF result.
  eos_pyateos:
      compare: true
      group:
          - mgmt
          - layer2
      test:
          - acl
      hostname: "{{ inventory_hostname }}"
      filter: true
      files: 
          - "{{ before_ids }}"
          - "{{ after_ids }}"
```