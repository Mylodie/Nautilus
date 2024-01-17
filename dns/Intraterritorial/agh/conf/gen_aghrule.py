#!/usr/bin/env python3

import urllib.request

# import idna

import os

# config start
dns_server_global = os.environ.get("DNS_SERVER_FALLBACK","EXAPMLE_DNS_SERVER_FALLBACK")
dns_server_cn = os.environ.get("DNS_SERVER_CN","udp://coredns")
agh_domain_rule_file = os.environ.get("AGH_DOMAIN_RULE_FILE", "./domain.rules")

accurl =""
dnsmasq_conf_url = "https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/master/accelerated-domains.china.conf"

url = accurl + dnsmasq_conf_url
agh_rules = [dns_server_global]

with urllib.request.urlopen(url) as response:
    file_contents = response.read()
    for line in file_contents.splitlines():
        domain = line.decode('utf-8').split("/")[1]
        # punycode = idna.encode(domain).decode("utf-8")
        punycode = domain
        agh_rule= "[/{}/]{}".format(punycode, dns_server_cn)
        agh_rules.append(agh_rule)

with open(agh_domain_rule_file, "w") as f:
    f.write("\n".join(agh_rules))

print("update AdguardHome DNS rule done.")