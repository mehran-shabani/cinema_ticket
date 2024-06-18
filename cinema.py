import uuid
import sqlite3

class Cinema:
    def __init__(self, name):
        self.cinema_id = str(uuid.uuid4())
        self.name = name
        self.save_to_db()

    def save_to_db(self):
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO cinemas (cinema_id, name)
        VALUES (?, ?)
        ''', (self.cinema_id, self.name))
        conn.commit()
        conn.close()

    def add_movie(self, movie):
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO movies (movie_id, title, rating, cinema_id)
        VALUES (?, ?, ?, ?)
        ''', (movie.movie_id, movie.title, movie.rating, self.cinema_id))
        conn.commit()
        conn.close()

    def update_cinema_details(self, name=None):
        if name:
            self.name = name
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE cinemas
        SET name = ?
        WHERE cinema_id = ?
        ''', (self.name, self.cinema_id))
        conn.commit()
        conn.close()

    def list_movies(self):
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT title FROM movies WHERE cinema_id = ?
        ''', (self.cinema_id,))
        movies = cursor.fetchall()
        conn.close()
        return [movie[0] for movie in movies]
