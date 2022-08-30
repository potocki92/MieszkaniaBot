import discord
import os
import sqlite3
from bs4 import BeautifulSoup
import requests
import re
from discord.ext import commands
from discord.ext import tasks
from webserver import keep_alive
from BeautifulSoupScrap import drop_table, print_all, read_from_db
from olx_bs import olx_scrap
from bno_bs import bno_scrap

# linki do scrapowania
URL = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/boleslawiec/'
URL_2 = 'https://boleslawiec.nieruchomosci-online.pl/mieszkania,wynajem/'


bot = commands.Bot(command_prefix='$')
db = sqlite3.connect('dane.db')
cur = db.cursor()

# token klienta discord
my_secret = os.environ['TOKEN']
client = discord.Client()




@tasks.loop(minutes=10)
async def test():
  channel = client.get_channel(955917326711132235)

  # OLX scrapper
  await olx_scrap('https://www.olx.pl/nieruchomosci/mieszkania/wynajem/boleslawiec/', cur, channel)
  await bno_scrap('https://boleslawiec.nieruchomosci-online.pl/mieszkania,wynajem/', cur, channel)
  
  db.commit()
  #end_parse


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

  # tworzenie tabeli w momencie kiedy ona nie istenieje
  cur.execute('''CREATE TABLE IF NOT EXISTS offers (name TEXT, price REAL, city TEXT, link BLOB)''')
  test.start()

# wysyłanie wiadomości do klienta Discord
@client.event
async def on_message(message):
  if message.author == client.user:
    return
    
  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')

  if message.content.startswith('$show'):
    await message.channel.send()

  if message.content.startswith('$drop'):
    drop_table()
    await message.channel.send('Table is clear!')

keep_alive()

client.run(my_secret)

