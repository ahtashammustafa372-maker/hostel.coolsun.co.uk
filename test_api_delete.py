import requests

try:
    url = "http://127.0.0.1:5000/api/tenants/2"
    print(f"Sending DELETE request to: {url}")
    response = requests.delete(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
