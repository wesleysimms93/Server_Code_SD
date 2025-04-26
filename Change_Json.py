import requests

url = "http://<your-server-ip>:5000/update_data"
data = {
    "key1": "value1",
    "key2": "value2"
}

response = requests.post(url, json=data)

print("Response status code:", response.status_code)
print("Response text:", response.text)