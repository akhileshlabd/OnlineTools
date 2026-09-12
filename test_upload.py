import urllib.request
import time

data = b"a" * (10 * 1024 * 1024)
req = urllib.request.Request("https://speed.cloudflare.com/__up", data=data, method="POST")

start = time.time()
try:
    with urllib.request.urlopen(req) as response:
        print(response.status)
except Exception as e:
    print(e)

print(f"Time: {time.time() - start} s")
