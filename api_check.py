import json

import requests

headers = {
    "Authorization": "Bearer qxrqatve9wzkpgqomdax"
}
params = {
    "exchange": "binance"
}

response = requests.get("", headers=headers, params=params).json()
with open("crypto_2.json", 'w') as f:
    json.dump(response, f)
