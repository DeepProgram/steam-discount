import time
from datetime import datetime,timedelta
import json
import requests
"""
data = {
  "searchkey":"discount",
  "value":"80"
  }
  
 data = {
  "searchkey":"price",
  "value":"20.00"
  }
"""
data = {
  "searchkey":"date",
  "value":"2022-08-06"
  }
response = requests.get("http://127.0.0.1:5000/getinfo",json=data)
print(response.text)
