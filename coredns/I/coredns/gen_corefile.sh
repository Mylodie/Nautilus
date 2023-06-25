#!/bin/sh
DOH_SERVER="$1"

china=`curl -sSL https://github.com/felixonmars/dnsmasq-china-list/raw/master/accelerated-domains.china.conf | while read line; do awk -F '/' '{print $2}' | grep -v '#' ; done |  paste -sd " " -`
apple=`curl -sSL https://github.com/felixonmars/dnsmasq-china-list/raw/master/apple.china.conf | while read line; do awk -F '/' '{print $2}' | grep -v '#' ; done |  paste -sd " " -`
google=`curl -sSL https://github.com/felixonmars/dnsmasq-china-list/raw/master/google.china.conf | while read line; do awk -F '/' '{print $2}' | grep -v '#' ; done |  paste -sd " " -`
cat>Corefile<<EOF
.:53 {
    ads {
       default-lists
       blacklist https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-domains.txt
       whitelist https://files.krnl.eu/whitelist.txt
       log
       auto-update-interval 24h
       list-store ads-cache
    }
    hosts {
        fallthrough
    }
    # choose your favourite DNS servers below
    forward . https://$DOH_SERVER/dns-query {
        except $china $apple $google dns.quad9.net cloudflare-dns.com dns.google dns.opendns.com
        # tls_servername $DOH_SERVER
        health_check 60s
    }
    forward . 223.5.5.5 114.114.114.114
    log
    cache
    # uncomment lines below to enable redis plugin
    #redisc {
    #    endpoint 127.0.0.1:6379
    #}
    health
    reload
}
EOF