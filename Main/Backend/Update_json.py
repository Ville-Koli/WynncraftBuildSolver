import requests
import json

response = requests.get("https://api.wynncraft.com/v3/item/database?fullResult")
if response.status_code == 200:
    data = response.json()
    with open('compress.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print("Updated compress.json")
else:
    print("Failed to fetch data")