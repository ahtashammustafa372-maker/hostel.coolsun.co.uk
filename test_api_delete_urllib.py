import urllib.request

url = "http://127.0.0.1:5000/api/tenants/2"
print(f"Sending DELETE request to: {url}")
req = urllib.request.Request(url, method="DELETE")
try:
    with urllib.request.urlopen(req) as response:
        print(f"Status Code: {response.getcode()}")
        print(f"Response Body: {response.read().decode()}")
except Exception as e:
    print(f"Request failed: {e}")
