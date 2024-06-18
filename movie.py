import uuid
import sqlite3

class Movie:
    def __init__(self, title, cinema_id):
        self.movie_id = str(uuid.uuid4())
        self.title = title
        self.rating = 0
        self.cinema_id = cinema_id
        self.save_to_db()

    def save_to_db(self):
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO movies (movie_id, title, rating, cinema_id)
        VALUES (?, ?, ?, ?)
        ''', (self.movie_id, self.title, self.rating, self.cinema_id))
        conn.commit()
        conn.close()

    def add_showtime(self, showtime):
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO showtimes (showtime_id, movie_id, showtime)
        VALUES (?, ?, ?)
        ''', (str(uuid.uuid4()), self.movie_id, showtime))
        conn.commit()
        conn.close()

    def update_movie_details(self, title=None, rating=None):
        if title:
            self.title = title
        if rating:
            self.rating = rating
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE movies
        SET title = ?, rating = ?
        WHERE movie_id = ?
        ''', (self.title, self.rating, self.movie_id))
        conn.commit()
        conn.close()

    def add_review(self, review):
        self.calculate_average_rating()

    def calculate_average_rating(self):
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT AVG(rating) FROM reviews WHERE movie_id = ?
        ''', (self.movie_id,))
        self.rating = cursor.fetchone()[0]
        cursor.execute('''
        UPDATE movies
        SET rating = ?
        WHERE movie_id = ?
        ''', (self.rating, self.movie_id))
        conn.commit()
        conn.close()
