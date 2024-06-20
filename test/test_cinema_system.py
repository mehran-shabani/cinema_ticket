import unittest
import sqlite3
import os
from cinema_system import CinemaSystem



def create_tables(db_name='test_cinema.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone_number INTEGER UNIQUE,
        password TEXT NOT NULL,
        birth_date TEXT NOT NULL,
        registration_date TEXT NOT NULL,
        last_login TEXT,
        wallet_balance REAL NOT NULL DEFAULT 0.0,
        subscription TEXT NOT NULL DEFAULT 'Bronze'
    )
    ''')
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
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS showtimes (
        showtime_id TEXT PRIMARY KEY,
        movie_id TEXT NOT NULL,
        showtime TEXT NOT NULL,
        FOREIGN KEY (movie_id) REFERENCES movies (movie_id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservations (
        reservation_id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        movie_id TEXT NOT NULL,
        showtime_id TEXT NOT NULL,
        seat_number TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (movie_id) REFERENCES movies (movie_id),
        FOREIGN KEY (showtime_id) REFERENCES showtimes (showtime_id)
    )
    ''')
    conn.commit()
    conn.close()


class TestCinemaSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # تنظیم یک پایگاه داده موقت برای تست
        cls.test_db = 'test_cinema.db'
        create_tables(cls.test_db)

    @classmethod
    def tearDownClass(cls):
        # حذف پایگاه داده موقت بعد از اتمام تست‌ها
        os.remove(cls.test_db)

    def setUp(self):
        # اطمینان از شروع هر تست با یک حالت تازه
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM reservations')
        cursor.execute('DELETE FROM showtimes')
        cursor.execute('DELETE FROM movies')
        cursor.execute('DELETE FROM cinemas')
        cursor.execute('DELETE FROM users')
        conn.commit()
        conn.close()

        self.cinema_system = CinemaSystem(self.test_db)

    def test_register_user(self):
        user = self.cinema_system.register_user("test_user", "test@example.com", "password123", "1990-01-01",
                                                "1234567890")
        self.assertIsNotNone(user.user_id)
        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.email, "test@example.com")

    def test_get_user_by_username(self):
        self.cinema_system.register_user("test_user", "test@example.com", "password123", "1990-01-01", "1234567890")
        user = self.cinema_system.get_user_by_username("test_user")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "test_user")

    def test_view_cinemas(self):
        self.cinema_system.add_cinema("Cinema One")
        cinemas = self.cinema_system.view_cinemas()
        self.assertEqual(len(cinemas), 1)
        self.assertEqual(cinemas[0].name, "Cinema One")

    def test_add_movie(self):
        cinema = self.cinema_system.add_cinema("Cinema One")
        movie = self.cinema_system.add_movie("Inception", cinema.cinema_id)
        self.assertIsNotNone(movie.movie_id)
        self.assertEqual(movie.title, "Inception")

    def test_add_showtime(self):
        cinema = self.cinema_system.add_cinema("Cinema One")
        movie = self.cinema_system.add_movie("Inception", cinema.cinema_id)
        showtime = self.cinema_system.add_showtime(movie.movie_id, "2024-12-31 20:00:00")
        self.assertIsNotNone(showtime.showtime_id)
        self.assertEqual(showtime.showtime, "2024-12-31 20:00:00")

    def test_make_reservation(self):
        user = self.cinema_system.register_user("test_user", "test@example.com", "password123", "1990-01-01",
                                                "1234567890")
        cinema = self.cinema_system.add_cinema("Cinema One")
        movie = self.cinema_system.add_movie("Inception", cinema.cinema_id)
        showtime = self.cinema_system.add_showtime(movie.movie_id, "2024-12-31 20:00:00")
        reservation = self.cinema_system.make_reservation(user.user_id, movie.movie_id, showtime.showtime_id, "A1")
        self.assertIsNotNone(reservation.reservation_id)
        self.assertEqual(reservation.user_id, user.user_id)
        self.assertEqual(reservation.seat_number, "A1")

    def test_view_reservations(self):
        user = self.cinema_system.register_user("test_user", "test@example.com", "password123", "1990-01-01",
                                                "1234567890")
        cinema = self.cinema_system.add_cinema("Cinema One")
        movie = self.cinema_system.add_movie("Inception", cinema.cinema_id)
        showtime = self.cinema_system.add_showtime(movie.movie_id, "2024-12-31 20:00:00")
        self.cinema_system.make_reservation(user.user_id, movie.movie_id, showtime.showtime_id, "A1")
        reservations = self.cinema_system.view_reservations(user.user_id)
        self.assertEqual(len(reservations), 1)
        self.assertEqual(reservations[0].seat_number, "A1")


if __name__ == '__main__':
    unittest.main()
