
from bs4 import BeautifulSoup
import requests
import asyncio
import re

def parse_price(price):
  return float(price.replace(' ','').replace('zł','').replace(',','.'))

@asyncio.coroutine
async def olx_scrap(URL, cur, channel):

  print("===================================")
  print("OLX SCRAP:")
  page = requests.get(URL)
  bs = BeautifulSoup(page.content, 'html.parser')

  for offer in bs.find_all('div', class_='offer-wrapper'):
    footer = offer.find('td', class_='bottom-cell')
    location = footer.find('small', class_='breadcrumb').get_text().strip()
    title = offer.find('strong').get_text().strip()
    price = parse_price(offer.find('p', class_='price').get_text().strip())
    links = ''
    for link in offer.find_all('a',attrs={'href': re.compile("^https://")}):
      links = str(link.get('href'))
      
    r = cur.execute('SELECT name FROM offers')
    rows = r.fetchall()

    # Komponent znajduje się już w bazie
    if (title,) in rows:
      print('Component "%s" found with rowid name'%title)

    # Komponent jeszcze nie znajduje się w bazie, więc jest dodawany do bazy danych oraz wysyłana jest wiadomość na discorda
    if not (title,) in rows:
      print( 'There is no component named %s'%title)
      
      cur.execute('INSERT INTO offers VALUES (?,?,?,?)', (title, price, location, links))
      await channel.send(title + ' ' + str(price) + ' ' + location)
      await channel.send(links)