import json
import unittest
import sqlite3
import os
import requests
import csv
import matplotlib.pyplot as plt


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

def join_ratings_and_boxOffice(cur, conn):
    cur.execute(
        """
        SELECT Ratings.views, Ratings.likes, BoxOfficeData.Amount
        FROM Ratings
        INNER JOIN BoxOfficeData 
        ON Ratings.id = BoxOfficeData.id
        """

    )

    res = cur.fetchall()
    conn.commit
    return res

def join_ratings_and_omdb(cur, conn):
    cur.execute(
        """
        SELECT Ratings.views, Ratings.likes, movie_data.imdb_rating, movie_data.runtime
        FROM Ratings
        INNER JOIN movie_data ON Ratings.id=movie_data.movie_id

        """

    )

    res = cur.fetchall()
    conn.commit
    return res

def join_titles_and_ratings(cur, conn):
    cur.execute(
        """
        SELECT Ratings.views, Ratings.likes, MovieTitlesData.Name
        FROM Ratings
        INNER JOIN MovieTitlesData ON Ratings.id=movieTitlesData.id

        """

    )

    res = cur.fetchall()
    conn.commit
    return res


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

def get_runtime_differences(cur, conn):
    runtimes = join_ratings_and_omdb(cur, conn)
    minutes_list = []
    list_of_differences = []
    sum = 0
    total = 100

    for tup in runtimes:
        minutes = tup[3]
        sum += minutes
        minutes_list.append(minutes)
    
    average = sum/total

    for minutes in minutes_list:
        difference = round(minutes-average)
        list_of_differences.append(difference)

    return(list_of_differences)


def imdb_to_boxOffice(cur, conn):
    imdb = join_ratings_and_omdb(cur, conn)
    boxOffice = join_ratings_and_boxOffice(cur, conn)
    sales_list = []
    imdb_rating_list = []

    for tup in boxOffice:
        sales = tup[2]
        if len(sales) == 12:
            int_sales = sales[1:4] + sales[5:8] + sales[9:12]
        else:
            int_sales = sales[1:3] + sales[4:7] + sales[8:11]

        sales_list.append(int(int_sales))
          
    
    for tup in imdb:
        imdb_rating = tup[2]
        imdb_rating_list.append(imdb_rating * 10000000)

    difference = [i / j for i, j in zip (imdb_rating_list, sales_list)]
    
    return(difference)


def titles (cur, conn):
    title_name = join_titles_and_ratings(cur, conn)
    list_of_titles = []
    
    for tup in title_name:
        name = tup[2]
        list_of_titles.append(name)

    return (list_of_titles)

def list_of_box_office_sales(cur, conn):
    sales_list  =[]
    boxOffice = join_ratings_and_boxOffice(cur, conn)
    for tup in boxOffice:
        sales = tup[2]
        if len(sales) == 12:
            int_sales = sales[1:4] + sales[5:8] + sales[9:12]
        else:
            int_sales = sales[1:3] + sales[4:7] + sales[8:11]

        sales_list.append(int(int_sales))
    
    return(sales_list)

def list_of_views():
    view_list = []
    for title in final_id_list:
        view = get_view_count(title)
        view_list.append(view)
    
    return(view_list)

def list_of_likes():
    like_list = []
    for title in final_id_list:
        like = get_like_count(title)
        like_list.append(like)
    
    return(like_list)

def list_of_imdb_ratings(cur, conn):
    imdb_rating_list = []
    imdb = join_ratings_and_omdb(cur, conn)
    for tup in imdb:
        imdb_rating = tup[2]
        imdb_rating_list.append(imdb_rating)
    return (imdb_rating_list)

def view_vs_boxoffice(cur, conn):
    x = list_of_views()
    y = list_of_box_office_sales(cur, conn)

    fig, ax = plt.subplots()

    ax.set_xlabel('Views per Movie Trailer')
    ax.set_ylabel('Box Office Sales ($)')
    ax.set_title('Do views per YouTube movie trailer affect box office sales?')

    plt.scatter(x, y, color = "purple")

    plt.show()

def like_vs_boxoffice(cur, conn):
    x = list_of_likes()
    y = list_of_box_office_sales(cur, conn)

    fig, ax = plt.subplots()

    ax.set_xlabel('Likes per Movie Trailer')
    ax.set_ylabel('Box Office Sales ($)')
    ax.set_title('Do likes per YouTube movie trailer affect box office sales?')

    plt.scatter(x, y, color = "purple")

    plt.show()

def view_vs_rating(cur, conn):
    x = list_of_views()
    y = list_of_imdb_ratings(cur, conn)

    fig, ax = plt.subplots()

    ax.set_xlabel('Views per Movie Trailer')
    ax.set_ylabel('IMDB Rating (scale of 1 to 10)')
    ax.set_title('Do views per YouTube movie trailer predict IMDb rating?')

    plt.scatter(x, y, color = "purple")

    plt.show()

def like_vs_rating(cur, conn):
    x = list_of_likes()
    y = list_of_imdb_ratings(cur, conn)

    fig, ax = plt.subplots()

    ax.set_xlabel('Likes per Movie Trailer')
    ax.set_ylabel('IMDB Rating (scale of 1 to 10)')
    ax.set_title('Do likes per YouTube movie trailer predict IMDb rating?')

    plt.scatter(x, y, color = "purple")

    plt.show()



    
def write_calculations(filename, cur, conn):
    header_list = ["Movie Title", "Like to View Ratio", "Difference From Average Runtime", "IMDB Rating to Box Office Sales Ratio(*10^7)"]

    with open(filename, "w+", newline = "") as f:
        write = csv.writer(f, delimiter = ',')
        write.writerow(header_list)

        ratio = like_to_view_calculations()
        diff = get_runtime_differences(cur, conn)
        ratio2 = imdb_to_boxOffice(cur, conn)
        title_names = titles(cur, conn)

        for i in range(100):
            write.writerow([title_names[i],ratio[i], diff[i], ratio2[i]])



title_list = get_movie_title(first_string) + get_movie_title(second_string)
cur, conn = open_database('movies.db')
make_ratings_table(final_id_list, cur, conn)
write_calculations("final_calculations.csv", cur, conn)
#view_vs_boxoffice(cur, conn)
#like_vs_boxoffice(cur, conn)
#view_vs_rating(cur, conn)
#like_vs_rating(cur, conn)

