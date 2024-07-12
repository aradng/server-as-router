#!/bin/bash

# send to correct iface and gateway
ip route add default via 31.14.122.33 table 200

# machine ip in secondary subnet
IP=$(ip route | grep 31.14.122.32/27 | awk '{print $9}')

# route packets originating from this machine with secondary subnet
ip rule add from $IP table 200 priority 100

# iptables RETURN target before docker DNAT for public facing iface
iptables -t nat -A PREROUTING ! -s 31.14.122.32/27 -i eth1 -j RETURN




