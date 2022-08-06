import time
from datetime import datetime,timedelta
import json
import requests
data = {
  "searchkey":"discount",
  "value":"0"
  }
response = requests.get("http://127.0.0.1:5000/getinfo",json=data)
print(response.text)