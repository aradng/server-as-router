# Server as Router
Make shift SOHO router from a Debian headless server.\
had a home setup with a tailscale subnet router and bunch of services running on my NUC decided to make that my router for some vpn and static routing shenanigans.


## Setup
Requires `python3`, `ipset`, `iptables` \
replace all instances of `ipset_net` and `code` inside ip2loc.py and commands and bash_scripts
### Country Forwarding
```shell
# create and flush ipset network with name ipset_net & populate with ip2location filtered country list matching code
python3 ip2loc.py

# ip and iptables rules for static routing
iptables -t mangle -A PREROUTING -m set --match-set [ipset_net] dst -j MARK --set-mark 100

# create table to match fwmark
ip rule add fwmark 100 table iran_table priority 100

# add default route to subnet router without VPN
ip route add table 100 default via [router_ip]

# make sure IP forwarding is enabled
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.conf
sysctl -p /etc/sysctl.conf
```
after setting up the above. if you need to add more countries or ipsets, create and populate another ipset network and repeat the mangle mark command for the corresponding ipset.\
theres an example for Valve's ASN below:
### Valve ASN.
```shell
# create valve ipset
ipset create valve nethash
# add ASN CIDRs
ipset add valve 162.254.192.0/21
ipset add valve 155.133.224.0/19
ipset add valve 185.25.180.0/22
ipset add valve 146.66.152.0/21
ipset add valve 208.64.200.0/22
ipset add valve 208.78.164.0/22
ipset add valve 192.69.96.0/22
# save ipset state
ipset save > /etc/iptables/ipset
# create another mark entry for valve ipset
iptables -t mangle -A PREROUTING -m set --match-set valve dst -j MARK --set-mark 100
```

## Reboot persistence 
if you're hapypy with the current config make config rules persist accross system reboots.\
makes sure your iptables rules are persistant as well with iptables-persistent or your distros counterpart
```shell
# save ipset state
ipset save > /etc/iptables/ipset

# create/enable ipset persistent service (has to start before restoring iptables rules)
cp services/ipset-persistent.service /etc/systemd/system
systemctl enable ipset-persistent.service

# create/enable automatic fetcher for ip2loc (default : run monthly)
cp services/ipset-fetch.service /etc/systemd/system
systemctl enable ipset-fetch.service

# create/enable ip rules to create table and routes after ipset is loaded 
#(default routers need to be available in the routing table before service start)
cp shells/static-routes.sh /etc/network
cp services/route-persistent.service /etc/systemd/system
systemctl enable route-persistent.service
```
