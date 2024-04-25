import json

import requests

api_key = "54d0320a-dc81-47c8-8f1c-217a128162f7"

headers = {
    "X-CMC_PRO_API_KEY": api_key,
    'Accepts': 'application/json'
}

params = {
    'start': 1,
    'limit': 5,
    'convert': 'USD'
}

url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

response = requests.get(url, headers=headers, params=params).json()
with open("crypt_info/crypto_2.json", 'w') as f:
    json.dump(response, f)
