import requests
from bs4 import BeautifulSoup

data = {
    'phone_number': '+79182124943'
}

url = 'https://web-telegram.ru/'
session = requests.Session()

txt = session.get(url)
print(txt.text)
