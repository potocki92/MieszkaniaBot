from bs4 import BeautifulSoup
import requests
import asyncio
import re

# usuwanie zbędnych znaków z ceny z OTODOM
def parse_price2(price):
  return float(price.replace('zł','').replace('/','').replace('mc',''))

@asyncio.coroutine
async def bno_scrap(URL, cur, channel):
  # Scrap boleslawiec.nieruchomosci-online
  #----------------------------------------------------
  headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }
  page = requests.get(URL, headers=headers)
  page.raise_for_status()
  
  bs = BeautifulSoup(page.text, 'html.parser')

  offer = bs.findAll('div', {'class':'column-container column_default'})

  print("===================================")
  print("BOLESLAWIEC-NIERUCHOMOSCI-ONLINE:")
  for item in offer[1].select('div.tertiary__wrapper  '):
    title = item.find({'h2':'name'}).text;
    location = item.find('span',{'class':'margin-right4'}).text;
    price = item.find('p',{'class':'title-a primary-display'});
    price = price.find('span').text;
    links = '';
    for link in item.find_all('a',attrs={'href': re.compile("^https://")}):
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