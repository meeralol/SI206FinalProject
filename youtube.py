import json
import unittest
import sqlite3
import os
import requests
import csv


API_KEY = "AIzaSyAtrqolfGTcMwKMlFDL3_EMMmNBtZJbuIo"

first_string = "id=TcMBFSGVi1c&id=7TavVZMewpY&id=wmiIUN-7qhE&id=Zi4LMpSDccc&id=Z1BCujX3pw8&id=8Qn_spdM5Zg&id=Nt9L1jCKGnE&id=VcBllhVj1eA&id=zAGVQLHvwOY&id=xhJ5P7Up3jA&id=rBxcF-r9Ibs&id=hNCmb-4oXJA&id=HZ7PAyCDwEg&id=M7XM597XO94&id=qLTDtbYmdWM&id=mYocfuqu2A8&id=bILE5BEyhdo&id=ELeMaP8EPAA&id=go6GEIrcvFY&id=WDkg3h8PCVU&id=xi-1NchUqMA&id=7NiYVoqBt-8&id=n0OFH4xpPr4&id=95ghQs5AmNk&id=QFxN2oDKk0E&id=EWw7rCHcduQ&id=zyYgDtY2AMY&id=cksYkEzUa7k&id=305sELs60kc&id=A6X4VAHdDVg&id=tu3mP0c51hE&id=S3vO8E2e6G0&id=w7pYhpJaJW8&id=zPXqwAGmX04&id=g4Hbz2jLxvQ&id=BV-WEb2oxLk&id=bCxm7cTpBAs&id=Ry9honCV3qc&id=id61hcbdMZA&id=ZlW9yhUKlkQ&id=isVtXH7n9lI&id=Vlya92LZqZw&id=YfkEQDPlb8g&id=1-q8C_c-nlM&id=jCyEX6u-Yhs&id=XrgVtuDRBjM&id=ksj69JaBrAo&id=T5z2EwJTr9I&id=-VLEPhfEN2M&id=BfTYY_pac8o"

first_id = first_string.split("&")

second_string = "id=lcwmDAYt22k&id=uOV-xMYQ7sk&id=VllcgXSIJkE&id=HeoLiTirRp4&id=QkZxoko_HC0&id=P6AaSMfXHbA&id=YVYzxm_RqMg&id=AbyJignbSj0&id=eIvbEC8N3cA&id=XtgCqMZofqM&id=VML6rQWssSk&id=km_L0v3C0ms&id=PM1DVbwKP3o&id=GqoEs4cG6Uw&id=1pKdCHvH310&id=RSKQ-lVsMdg&id=tKwhs5u9z8c&id=G6Th84oGDno&id=52bORzIODec&id=N_QksSzK7sI&id=H6MLJG0RdDE&id=AST2-4db4ic&id=aKXvex7b1Ew&id=_j5hwooOHVE&id=z9CEIcmWmtA&id=BGyieGVn4P4&id=0phuNQQ_gHI&id=BOzFZxB-8cw&id=nv5FD7NLHCc&id=ZKsc2I4Tgsk&id=9eY2W7uUkDE&id=PeHNLikDiVw&id=ZtYTwUxhAoI&id=IeXqWDFJZiw&id=aSGFt6w0wok&id=BVZDhunTrYA&id=1Vnghdsjmd0&id=mP0VHJYFOAU&id=Dp2ufFO4QGg&id=TZsgNH17_X4&id=vTfJp2Ts9X8&id=98t7aXRaA6w&id=_BcYBFC6zfY&id=WqF3VTv0cqU&id=28dHbIR_NB4&id=A2FrrSyyKfA&id=VjGJm3wV5-I&id=5xH0HfJHsaY&id=i5l6a5RiR1E&id=AvXjx8SZbv8"

second_id = second_string.split("&")

final_id_list = first_id + second_id

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def get_request_url(string):
    url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&{string}&key={API_KEY}"
    return (url)


def get_view_count(string):
    url = get_request_url(string)
    response = requests.get(url)
    data = json.loads(response.text)

    viewCount = data['items'][0]['statistics']['viewCount']


    return(int(viewCount))


def get_like_count(string):
    url = get_request_url(string)
    response = requests.get(url)
    data = json.loads(response.text)

    likeCount = data['items'][0]['statistics']['likeCount']
        
    return (int(likeCount))


def get_movie_title(string):
    url = get_request_url(string)
    response = requests.get(url)
    data = json.loads(response.text)

    title_list = []

    for item in data['items']:
        snippet = item['snippet']
        title = snippet['title']
        title_list.append(title)
    
    return (title_list)



def make_ratings_table(final_id_list, cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS Ratings (id INTEGER PRIMARY KEY, views INTEGER, likes INTEGER)')

    cur.execute('SELECT id FROM Ratings WHERE id = (SELECT MAX (id) FROM Ratings)')

    count = 0

    start = cur.fetchone()
    
    if (start == None):
        start = 0
    else:
        start = start[0] + 1
   
    for title in final_id_list[start: start + 25]:
        id = start + count
        view = get_view_count(title)
        like = get_like_count(title)
        cur.execute('INSERT OR IGNORE INTO Ratings (id, views, likes) VALUES (?, ?, ?)',(id, view, like)) 
        
        count += 1
    
    conn.commit()

def like_to_view_calculations():
    view_list = []
    like_list = []
    for title in final_id_list:
        view = get_view_count(title)
        view_list.append(view)
        like = get_like_count(title)
        like_list.append(like)

    calc = [i / j for i, j in zip (like_list, view_list)]
    
    return calc
    
def write_calculations(filename):
    header_list = ["Movie Title", "Like to View Ratio", "Distributor Percentage", "Difference From Average Runtime"]

    with open(filename, "w+", newline = "") as f:
        write = csv.writer(f, delimiter = ',')
        write.writerow(header_list)

        ratio = like_to_view_calculations()

        # write.writerow(['', ratio, '', '']) 


title_list = get_movie_title(first_string) + get_movie_title(second_string)
cur, conn = open_database('movies.db')
# make_ratings_table(final_id_list, cur, conn)
write_calculations("final_calculations.csv")

