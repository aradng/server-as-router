#!/bin/bash
# machine ip and iface in secondary subnet
GATEWAY=31.14.122.33
SUBNET=31.14.122.32/27
IP=$(ip route | grep $SUBNET | awk '{print $9}')
IFACE=$(ip route | grep $SUBNET | awk '{print $3}')

# send to correct iface and gateway
ip route add default via $GATEWAY table 200

# route packets originating from this machine with secondary subnet
ip rule add from $IP table 200 priority 100

# iptables RETURN target before docker DNAT for public facing iface
iptables -t nat -I PREROUTING ! -s $SUBNET -i $IFACE -j RETURN




