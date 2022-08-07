import requests

data = {
    "search key": "date",
    "value": "2022-08-07"
}
response = requests.get("http://127.0.0.1:5000/getinfo", json=data)
print(response.text)
 
