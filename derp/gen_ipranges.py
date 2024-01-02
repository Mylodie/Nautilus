from netaddr import IPNetwork, IPSet
import urllib.request

# Full set, I .e. all possible IPv4 addresses
full_set = IPSet([IPNetwork('0.0.0.0/0')])

# 给定的 IP 区间列表
reserved_cidrs = [
    '0.0.0.0/8',
    '10.0.0.0/8',
    '127.0.0.0/8',
    '169.254.0.0/16',
    '172.16.0.0/12',
    '192.168.0.0/16',
    '224.0.0.0/4',
    '240.0.0.0/4'
]

china_cidrs_url = "https://raw.githubusercontent.com/17mon/china_ip_list/master/china_ip_list.txt"
with urllib.request.urlopen(china_cidrs_url) as response:
    file_contents = response.read()
    china_cidrs = [l.decode('utf-8') for l in file_contents.splitlines()] 
        
# Subtract the given IP range from the full set.
for cidr in reserved_cidrs + china_cidrs:
    full_set.remove(IPNetwork(cidr))

ex_cidrs = [str(iprange) for iprange in full_set.iter_cidrs()]

with open("extraterritorial_ipranges.txt","w+") as f:
    f.write(",".join(ex_cidrs))





