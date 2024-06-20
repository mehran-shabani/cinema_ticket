import unittest
import sqlite3
import os
from movie import Movie
import uuid


def create_tables(db_name='test_cinema.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cinemas (
        cinema_id TEXT PRIMARY KEY,
        name TEXT NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        movie_id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        rating REAL NOT NULL DEFAULT 0.0,
        cinema_id TEXT NOT NULL,
        FOREIGN KEY (cinema_id) REFERENCES cinemas (cinema_id)
    )
    ''')
    conn.commit()
    conn.close()


class TestMovie(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up a temporary database for testing
        cls.test_db = 'test_cinema.db'
        create_tables(cls.test_db)

    @classmethod
    def tearDownClass(cls):
        # Remove the temporary database after tests
        os.remove(cls.test_db)

    def setUp(self):
        # Ensure each test starts with a fresh state
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM movies')
        cursor.execute('DELETE FROM cinemas')
        cursor.execute('INSERT INTO cinemas (cinema_id, name) VALUES (?, ?)', (str(uuid.uuid4()), 'Cinema One'))
        conn.commit()
        conn.close()

    def test_create_movie(self):
        movie = Movie.create_movie('Inception', 'Cinema One', db=self.test_db)
        self.assertIsNotNone(movie.movie_id)
        self.assertEqual(movie.title, 'Inception')
        self.assertEqual(movie.rating, 0.0)
        self.assertEqual(movie.cinema_id, 'Cinema One')

    def test_get_movie_by_id(self):
        movie = Movie.create_movie('Inception', 'Cinema One', db=self.test_db)
        fetched_movie = Movie.get_movie_by_id(movie.movie_id, db=self.test_db)
        self.assertIsNotNone(fetched_movie)
        self.assertEqual(fetched_movie.title, 'Inception')

    def test_get_movies_by_cinema_id(self):
        movie1 = Movie.create_movie('Inception', 'Cinema One', db=self.test_db)
        movie2 = Movie.create_movie('Interstellar', 'Cinema One', db=self.test_db)
        movies = Movie.get_movies_by_cinema_id('Cinema One', db=self.test_db)
        self.assertEqual(len(movies), 2)
        self.assertEqual(movies[0].title, 'Inception')
        self.assertEqual(movies[1].title, 'Interstellar')


if __name__ == '__main__':
    unittest.main()
