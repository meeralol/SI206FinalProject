
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from bs4 import BeautifulSoup
import requests
from datetime import date
from xml.sax import parseString
import os
import json
import sqlite3



def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def boxofficeurl(url):
    url="https://www.boxofficemojo.com/year/2019/?grossesOption=calendarGrosses&sort=rank&sortDir=asc"
    return url


def getmovielist(url):
    x = boxofficeurl(url)
    req=requests.get(x)
    content=req.text

    soup=BeautifulSoup(content, features="lxml")

    findmovies = soup.find_all('td', class_="a-text-left mojo-field-type-release mojo-cell-wide")

    nameslist = []
    for item in findmovies:
        nameslist.append(item.select('a')[0].string)

    finalnameslist = nameslist[0:100]
    
    return finalnameslist


    
def getboxlist(url):
    x = boxofficeurl(url)
    req=requests.get(x)
    content=req.text

    soup=BeautifulSoup(content, features="lxml")
    boxoffice = soup.find_all('td', class_="a-text-right mojo-field-type-money mojo-estimatable")

    boxlist = []
    for movie in boxoffice:
        m = movie.text
        boxlist.append(m)

    boxlist = boxlist[::2]
    boxlist = boxlist[0:100]
    

    return boxlist


def make_boxoffice_table(boxlist, cur, conn):
    cur.execute('DROP TABLE IF EXISTS BoxOfficeData')
    cur.execute('CREATE TABLE IF NOT EXISTS BoxOfficeData (ID INTEGER PRIMARY KEY, Amount INTEGER)')

    id = 1
    for i in range(len(boxlist)):
        cur.execute('INSERT INTO BoxOfficeData (ID, Amount) VALUES (?, ?)',(id, boxlist[i])) 
        id += 1
    conn.commit()

def make_names_table(nameslist, cur, conn):
    cur.execute('DROP TABLE IF EXISTS MovieTitlesData')
    cur.execute('CREATE TABLE IF NOT EXISTS MovieTitlesData (ID INTEGER PRIMARY KEY, Name INTEGER)')

    id = 1
    for i in range(len(nameslist)):
        cur.execute('INSERT INTO MovieTitlesData (ID, Name) VALUES (?, ?)',(id, nameslist[i])) 
        id += 1
    conn.commit()



boxlist = getboxlist("https://www.boxofficemojo.com/year/2019/?grossesOption=calendarGrosses&sort=rank&sortDir=asc")
nameslist = getmovielist("https://www.boxofficemojo.com/year/2019/?grossesOption=calendarGrosses&sort=rank&sortDir=asc")
cur, conn = open_database('boxofficedata.db')
make_boxoffice_table(boxlist, cur, conn)
make_names_table(nameslist, cur, conn)







