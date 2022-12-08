import json
import unittest
import sqlite3
import os
import requests


API_KEY = "AIzaSyAtrqolfGTcMwKMlFDL3_EMMmNBtZJbuIo"

first_string = "id=TcMBFSGVi1c&id=7TavVZMewpY&id=wmiIUN-7qhE&id=Zi4LMpSDccc&id=Z1BCujX3pw8&id=8Qn_spdM5Zg&id=Nt9L1jCKGnE&id=VcBllhVj1eA&id=zAGVQLHvwOY&id=xhJ5P7Up3jA&id=rBxcF-r9Ibs&id=hNCmb-4oXJA&id=HZ7PAyCDwEg&id=M7XM597XO94&id=qLTDtbYmdWM&id=mYocfuqu2A8&id=bILE5BEyhdo&id=ELeMaP8EPAA&id=go6GEIrcvFY&id=WDkg3h8PCVU&id=xi-1NchUqMA&id=7NiYVoqBt-8&id=n0OFH4xpPr4&id=95ghQs5AmNk&id=QFxN2oDKk0E&id=EWw7rCHcduQ&id=zyYgDtY2AMY&id=cksYkEzUa7k&id=305sELs60kc&id=A6X4VAHdDVg&id=tu3mP0c51hE&id=S3vO8E2e6G0&id=w7pYhpJaJW8&id=zPXqwAGmX04&id=g4Hbz2jLxvQ&id=BV-WEb2oxLk&id=bCxm7cTpBAs&id=Ry9honCV3qc&id=id61hcbdMZA&id=ZlW9yhUKlkQ&id=isVtXH7n9lI&id=Vlya92LZqZw&id=YfkEQDPlb8g&id=1-q8C_c-nlM&id=jCyEX6u-Yhs&id=XrgVtuDRBjM&id=ksj69JaBrAo&id=T5z2EwJTr9I&id=-VLEPhfEN2M&id=BfTYY_pac8o"

second_string = "id=lcwmDAYt22k&id=uOV-xMYQ7sk&id=VllcgXSIJkE&id=HeoLiTirRp4&id=QkZxoko_HC0&id=P6AaSMfXHbA&id=YVYzxm_RqMg&id=AbyJignbSj0&id=eIvbEC8N3cA&id=XtgCqMZofqM&id=VML6rQWssSk&id=km_L0v3C0ms&id=PM1DVbwKP3o&id=GqoEs4cG6Uw&id=1pKdCHvH310&id=RSKQ-lVsMdg&id=tKwhs5u9z8c&id=G6Th84oGDno&id=52bORzIODec&id=N_QksSzK7sI&id=H6MLJG0RdDE&id=AST2-4db4ic&id=aKXvex7b1Ew&id=_j5hwooOHVE&id=z9CEIcmWmtA&id=BGyieGVn4P4&id=0phuNQQ_gHI&id=BOzFZxB-8cw&id=nv5FD7NLHCc&id=ZKsc2I4Tgsk&id=9eY2W7uUkDE&id=PeHNLikDiVw&id=ZtYTwUxhAoI&id=IeXqWDFJZiw&id=aSGFt6w0wok&id=BVZDhunTrYA&id=1Vnghdsjmd0&id=mP0VHJYFOAU&id=Dp2ufFO4QGg&id=TZsgNH17_X4&id=vTfJp2Ts9X8&id=98t7aXRaA6w&id=_BcYBFC6zfY&id=WqF3VTv0cqU&id=28dHbIR_NB4&id=A2FrrSyyKfA&id=VjGJm3wV5-I&id=5xH0HfJHsaY&id=i5l6a5RiR1E&id=AvXjx8SZbv8"

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def get_request_url(string):
    url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&{string}&key={API_KEY}"
    return (url)

# def get_data(string):
#     url = get_request_url(string)
#     response = requests.get(url)
#     data = json.loads(response.text)

#     viewCountList = []
#     likeCountList = []

#     for item in data['items']:
#         stats = item['statistics']
#         viewCount = stats['viewCount']
#         likeCount = stats['likeCount']
#         viewCountList.append(int(viewCount))
#         likeCountList.append(int(likeCount))

    
    
    
#     print(likeCountList)


def get_view_count(string):
    url = get_request_url(string)
    response = requests.get(url)
    data = json.loads(response.text)

    viewCountList = []

    for item in data['items']:
        stats = item['statistics']
        viewCount = stats['viewCount']
        viewCountList.append(int(viewCount))
    
    return(viewCountList)

def get_like_count(string):
    url = get_request_url(string)
    response = requests.get(url)
    data = json.loads(response.text)

    likeCountList = []

    for item in data['items']:
        stats = item['statistics']
        likeCount = stats['likeCount']
        likeCountList.append(int(likeCount))
    return (likeCountList)

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

def make_title_table(title_list, cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS Titles (id INTEGER PRIMARY KEY, title TEXT)')

    id = 1
    for title in title_list:
        cur.execute('INSERT INTO Titles (id, title) VALUES (?, ?)',(id,title)) 
        id += 1
    conn.commit()

def make_ratings_table(title_list, cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS Titles (id INTEGER PRIMARY KEY, title TEXT)')

    id = 1
    for title in title_list:
        cur.execute('INSERT INTO Titles (id, title) VALUES (?, ?)',(id,title)) 
        id += 1
    conn.commit()

list_of_views = get_view_count(first_string) + get_view_count(second_string)
list_of_likes = get_like_count(first_string) + get_like_count(second_string)
title_list = get_movie_title(first_string) + get_movie_title(second_string)



cur, conn = open_database('titles.db')
make_title_table(title_list, cur, conn)
