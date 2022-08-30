from bs4 import BeautifulSoup
import sqlite3
import requests
import re

URL = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/boleslawiec/'

db = sqlite3.connect('dane.db')
cur = db.cursor()


def drop_table():
  cur.execute("DROP TABLE offers")


def read_from_db():
  cur.execute("SELECT name FROM offers")
  for row in cur.fetchall():
    print(row)

# Drukowanie całej bazy danych
def select_all_tasks(db):
    """
    Query all rows in the offers table
    :param conn: the Connection object
    :return:
    """

    for row in cur.execute('SELECT * FROM offers'):
      print(row)
      
# create a database connection

def print_all():
  with db:
    print("Query all tasks")
    select_all_tasks(db)
