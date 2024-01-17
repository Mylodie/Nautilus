from urllib.request import Request, urlopen

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

url_list = [
    "https://raw.githubusercontent.com/lord-alfred/ipranges/main/all/ipv4_merged.txt",
    "https://www.cloudflare.com/ips-v4",
]

ex_ipranges = []

for url in url_list:
    with urlopen(
        Request(
            url=url,
            headers=headers,
        )
    ) as response:
        ex_ipranges += [l.decode("utf-8") for l in response.read().splitlines()]

with open("ex_ipranges.txt", "w") as f:
    f.write("\n".join(ex_ipranges))
    print(len(ex_ipranges))