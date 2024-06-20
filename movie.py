import uuid
import sqlite3

class Movie:
    def __init__(self, movie_id, title, rating, cinema_id):
        self.movie_id = movie_id
        self.title = title
        self.rating = rating
        self.cinema_id = cinema_id

    @staticmethod
    def create_movie(title, cinema_id):
        movie_id = str(uuid.uuid4())
        movie = Movie(movie_id, title, 0.0, cinema_id)
        movie.save_to_db()
        return movie

    def save_to_db(self):
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO movies (movie_id, title, rating, cinema_id)
        VALUES (?, ?, ?, ?)
        ''', (self.movie_id, self.title, self.rating, self.cinema_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_movie_by_id(movie_id):
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM movies WHERE movie_id = ?
        ''', (movie_id,))
        movie_data = cursor.fetchone()
        conn.close()
        if movie_data:
            return Movie(*movie_data)
        return None

    @staticmethod
    def get_movies_by_cinema_id(cinema_id):
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM movies WHERE cinema_id = ?
        ''', (cinema_id,))
        movies_data = cursor.fetchall()
        conn.close()
        return [Movie(*movie_data) for movie_data in movies_data]
