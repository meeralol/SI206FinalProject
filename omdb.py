import requests
import unittest
import sqlite3
import json
import matplotlib
import os

api_key = "eff62a1c"

def get_data_url(movie):
    url = f"http://www.omdbapi.com/?{movie}&apikey={api_key}"
    return url

def get_title(movie):
    url = get_data_url(movie)
    response = requests.get(url)
    data = json.loads(response.text)
    title = data['Title']

    return title


def get_imdb_rating(movie):
    url = get_data_url(movie)
    response = requests.get(url)
    data = json.loads(response.text)
    rating = data['imdbRating']

    return rating


def create_imdb_table(movie_titles, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS movie_data (movie_id INTEGER PRIMARY KEY, imdb_rating INTEGER)")

    cur.execute("SELECT movie_id FROM movie_data WHERE movie_id = (SELECT MAX(movie_id) FROM movie_data)")

    count = 0

    for movie in movie_titles:
        count += 1
        movie_id = count
        title = get_title(movie)
        imdb_rating = get_imdb_rating(movie)
  
        cur.execute("INSERT OR IGNORE INTO movie_data (movie_id, imdb_rating) VALUES (?, ?)", (movie_id, imdb_rating))

        conn.commit()


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'movies.db')
    cur = conn.cursor()

    movie_titles = ["t=avengers%3A+endgame", "t=the+lion+king&y=2019", "t=toy+story+4", "t=frozen+2", "t=captain+marvel", "t=Star+Wars%3A+Episode+IX+%E2%80%93+The+Rise+of+Skywalker", "t=Spider-Man%3A+Far+from+Home", "t=Aladdin", "t=Joker", "t=It+Chapter+Two", "t=Jumanji%3A+The+Next+Level", "t=Us", "t=Fast+%26+Furious+Presents%3A+Hobbs+%26+Shaw", "t=John+Wick%3A+Chapter+3+-+Parabellum", "t=How+to+Train+Your+Dragon%3A+The+Hidden+World", "t=The+Secret+Life+of+Pets+2", "t=Pok%C3%A9mon+Detective+Pikachu", "t=Once+Upon+a+Time+in+Hollywood", "t=Shazam!", "t=Aquaman", "t=Knives+Out", "t=Dumbo&y=2019", "t=Maleficent%3A+Mistress+of+Evil", "t=Glass", "t=Godzilla%3A+King+of+the+Monsters", "t=The+Upside", "t=Ford+v+Ferrari", "t=The+Lego+Movie+2%3A+The+Second+Part", "t=Hustlers", "t=The+Addams+Family", "t=Downton+Abbey&y=2019", "t=Rocketman", "t=Alita%3A+Battle+Angel", "t=Good+Boys", "t=Spider-Man%3A+Into+the+Spider-Verse", "t=Men+in+Black%3A+International", "t=Annabelle+Comes+Home", "t=Yesterday", "t=A+Madea+Family+Funeral", "t=Zombieland%3A+Double+Tap", "t=Angel+Has+Fallen", "t=Scary+Stories+to+Tell+in+the+Dark", "t=Mary+Poppins+Returns", "t=X-Men%3A+Dark+Phoenix", "t=Terminator%3A+Dark+Fate", "t=Abominable", "t=Dora+and+the+Lost+City+of+Gold", "t=Escape+Room", "t=A+Beautiful+Day+in+the+Neighborhood", "t=Midway", "t=Bumblebee", "t=The+Curse+of+La+Llorona", "t=Pet+Sematary&y=2019", "t=What+Men+Want", "t=Green+Book", "t=Ad+Astra", "t=isn't+it+romantic", "t=Gemini+Man", "t=Ma", "t=Five+Feet+Apart", "t=Wonder+Park", "t=Rambo%3A+Last+Blood", "t=Playing+with+Fire", "t=Harriet", "t=A+Dog%E2%80%99s+Way+Home", "t=The+Angry+Birds+Movie+2", "t=Little", "t=Queen+%26+Slim", "t=Breakthrough", "t=The+Mule", "t=Crawl", "t=Little+Women", "t=The+Intruder", "t=The+Hustle", "t=Last+Christmas", "t=Overcomer", "t=Cold+Pursuit", "t=Doctor+Sleep", "t=Dragon+Ball+Super%3A+Broly", "t=Long+Shot", "t=Spies+in+Disguise", "t=Child%E2%80%99s+Play&y=2019", "t=Ready+or+Not", "t=Happy+Death+Day+2U", "t=Vice", "t=21+Bridges", "t=Midsommar", "t=Bohemian+Rhapsody", "t=The+Art+of+Racing+in+the+Rain", "t=Countdown", "t=Uncut+Gems", "t=Judy", "t=Ralph+Breaks+the+Internet", "t=Fighting+with+My+Family", "t=On+the+Basis+of+Sex", "t=A+Dog%E2%80%99s+Journey", "t=Booksmart", "t=Parasite", "t=Stuber", "t=47+Meters+Down%3A+Uncaged"]

    create_imdb_table(movie_titles, cur, conn)

if __name__ == "__main__":
    main()

