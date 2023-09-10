#!/bin/bash
# create table iran_table with fwmark 100 match all iran traffic marked in iptables PREROUTING according to ipset
ip rule add fwmark 100 table iran_table priority 100
# add default route to non-vpn gateway
ip route add default via 192.168.0.1 table 100