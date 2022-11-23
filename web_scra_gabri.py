import requests
from bs4 import BeautifulSoup


ender = requests.get(f'https://br.investing.com/currencies/usd-brl')
ender_get = ender.content
bea = BeautifulSoup(ender_get, 'html.parser')

print(bea)


