import requests

URL = "https://getpantry.cloud/apiv1/pantry/cebe6650-5045-4ea3-b6f0-d171a877b307/basket/testbasket"
API = "cebe6650-5045-4ea3-b6f0-d171a877b307"

def place(data):
    requests.put(URL,json=data)

def ask():
    res = requests.get(URL)
    data = res.json()
    return data
      