
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from bs4 import BeautifulSoup
import requests
from datetime import date
from xml.sax import parseString
import os
import json
import sqlite3

def read_data(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(full_path)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    return json_data

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def make_dicts(url):
    url="https://www.boxofficemojo.com/year/2019/?grossesOption=calendarGrosses&sort=rank&sortDir=asc"

    req=requests.get(url)
    content=req.text

    soup=BeautifulSoup(content, features="lxml")


#print(content)

# Fun and Frustration : class = "a-text-right mojo-field-type-money mojo-estimatable"

    boxoffice = soup.find_all('td', class_="a-text-right mojo-field-type-money mojo-estimatable")
    findmovies = soup.find_all('td', class_="a-text-left mojo-field-type-release mojo-cell-wide")

#print(boxoffice)
#print(len(boxoffice))



    nameslist = []
    for item in findmovies:
        nameslist.append(item.select('a')[0].string)

    finalnameslist = nameslist[0:100]
    print("final names list")
    print(finalnameslist)
    print("length " + str(len(finalnameslist)))

    boxlist = []
    for movie in boxoffice:
        m = movie.text
        boxlist.append(m)

    boxlist = boxlist[::2]

    #print("the length of finalnameslist is " + str(len(finalnameslist)))
    #print(finalnameslist)

   
    #print(boxlist)
    #print(len(boxlist))

    combinedict = {}

    for i in range(len(finalnameslist)):
        combinedict[finalnameslist[i]] = boxlist[i]

    print(" ")
    print(combinedict)
    print(len(combinedict.keys()))

def make_boxoffice_table(cur, conn):
    cur.execute('DROP TABLE IF EXISTS Box Office Data')
    cur.execute('CREATE TABLE Box Office Data (name TEXT PRIMARY KEY, Name STRING, Gross Domestic Box Office Sales INTEGER')

    for i in range(len(nameslist)):
        cur.execute("INSERT INTO Box Office Data (Name, Gross Domestic Box Office Sales) VALUES (?,?)",(nameslist[i], boxlist[i]))
    conn.commit()


def main():
    make_dicts(url="https://www.boxofficemojo.com/year/2019/?grossesOption=calendarGrosses&sort=rank&sortDir=asc")


if __name__ == "__main__":
    main()


