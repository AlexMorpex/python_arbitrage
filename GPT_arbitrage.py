import requests


response = requests.get('https://ascendex.com/api/pro/v1/ticker')
for el in response.json()['data']:
    if el['symbol'] == "KAI/USDT":
        print(el['ask'])
