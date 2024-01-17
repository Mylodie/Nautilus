import http.client
import ssl
import sys
import base64
from urllib.parse import urlencode
import struct
import socket

def build_dns_query(domain):
    # DNS header: ID, QR, Opcode, AA, TC, RD, RA, Z, RCODE
    header = b'\x00\x01\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'
    # DNS question: QNAME, QTYPE, QCLASS
    qname = b''.join(len(part).to_bytes(1, 'big') + part.encode() for part in domain.split('.')) + b'\x00'
    qtype = b'\x00\x01'
    qclass = b'\x00\x01'
    return header + qname + qtype + qclass

def decode_dns_message(data):
    # parse header
    id, flags, qdcount, ancount, nscount, arcount = struct.unpack('!6H', data[:12])
    header = {
        'ID': id,
        'Flags': flags,
        'QDCount': qdcount,
        'ANCount': ancount,
        'NSCount': nscount,
        'ARCount': arcount,
    }

    # skip question
    offset = data.index(b'\x00', 12) + 5

    # parse answer
    answers = []
    for _ in range(ancount):
        # skip NAME、TYPE、CLASS and TTL
        offset = data.index(b'\x00', offset) + 11
        # parse IP addr
        ip_address = socket.inet_ntoa(data[offset:offset+4])
        answers.append(ip_address)
        offset += 4

    return {
        'Header': header,
        'Answers': answers,
    }

def dns_over_https(server, query):
    context = ssl._create_unverified_context()

    server_url = server.split("/")
    host_port = server_url[2].split(":")
    host = host_port[0]
    port = int(host_port[1])

    conn = http.client.HTTPSConnection(host, port, context=context)

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    }

    dns_query = build_dns_query(query)
    dns_query_base64 = base64.urlsafe_b64encode(dns_query).rstrip(b'=')
    params = urlencode({"dns": dns_query_base64})
    conn.request("GET", "/dns-query?" + params, headers=headers)
    
    response = conn.getresponse()

    if response.status == 200:
        data = response.read()
        print(decode_dns_message(data))
    else:
        print(response.read())
        print("Error: " + str(response.status) + " " + response.reason)
    conn.close()

if __name__ == "__main__":
    dns_over_https(sys.argv[1], sys.argv[2])
