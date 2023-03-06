import requests
import re

base_url = 'https://api3.binance.com'

symbol = input('Digite o símbolo: ')

pattern = r"^[a-zA-Z][-a-zA-Z0-9]*[A-Z]{2,}$"

if re.match(pattern, symbol):
    print("O símbolo é válido.")
else:
    print("O símbolo é inválido.")

# coinapi_apikey = ''

url = base_url + '/api/v3/avgPrice'

params={'symbol': 'BTCUSDT'}

response = requests.get(url, params=params)

print(response.text)

