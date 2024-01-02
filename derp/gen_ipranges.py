from urllib.request import Request, urlopen

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


# lord_alfred_ipranges
# - google
# - Bing
# - AWS
# - Microsoft(Azure)
# - Oracle
# - DO
# - GH
# - FB
# - TW
# - Linode
# - TG
# - OpenAI

with urlopen(
    Request(
        url="https://raw.githubusercontent.com/lord-alfred/ipranges/main/all/ipv4_merged.txt",
        headers=headers,
    )
) as response:
    lord_alfred_ipranges = [l.decode("utf-8") for l in response.read().splitlines()]
#

with urlopen(
    Request(url="https://www.cloudflare.com/ips-v4", headers=headers)
) as response:
    cloudflare_ipranges = [l.decode("utf-8") for l in response.read().splitlines()]
#

with open("ex_ipranges.txt", "w+") as f:
    f.write("\n".join(lord_alfred_ipranges + cloudflare_ipranges))
