import unittest
import sqlite3
import os
import uuid
from reservation import Reservation


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


class TestReservation(unittest.TestCase):
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

        # اضافه کردن داده‌های نمونه برای کاربران، سینماها، فیلم‌ها و زمان‌های نمایش
        cursor.execute(
            'INSERT INTO users (user_id, username, email, phone_number, password, birth_date, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (str(uuid.uuid4()), 'john_doe', 'john@example.com', 1234567890, 'password', '1990-01-01', '2024-01-01'))
        cinema_id = str(uuid.uuid4())
        cursor.execute('INSERT INTO cinemas (cinema_id, name) VALUES (?, ?)', (cinema_id, 'Cinema One'))
        movie_id = str(uuid.uuid4())
        cursor.execute('INSERT INTO movies (movie_id, title, cinema_id) VALUES (?, ?, ?)',
                       (movie_id, 'Inception', cinema_id))
        showtime_id = str(uuid.uuid4())
        cursor.execute('INSERT INTO showtimes (showtime_id, movie_id, showtime) VALUES (?, ?, ?)',
                       (showtime_id, movie_id, '2024-12-31 20:00:00'))
        conn.commit()
        conn.close()

    def test_create_reservation(self):
        user_id = self._get_user_id('john_doe')
        movie_id = self._get_movie_id('Inception')
        showtime_id = self._get_showtime_id(movie_id)
        reservation = Reservation.create_reservation(user_id, movie_id, showtime_id, 'A1', db=self.test_db)
        self.assertIsNotNone(reservation.reservation_id)
        self.assertEqual(reservation.user_id, user_id)
        self.assertEqual(reservation.movie_id, movie_id)
        self.assertEqual(reservation.showtime_id, showtime_id)
        self.assertEqual(reservation.seat_number, 'A1')
        self.assertEqual(reservation.status, 'reserved')

    def test_get_reservation_by_id(self):
        user_id = self._get_user_id('john_doe')
        movie_id = self._get_movie_id('Inception')
        showtime_id = self._get_showtime_id(movie_id)
        reservation = Reservation.create_reservation(user_id, movie_id, showtime_id, 'A1', db=self.test_db)
        fetched_reservation = Reservation.get_reservation_by_id(reservation.reservation_id, db=self.test_db)
        self.assertIsNotNone(fetched_reservation)
        self.assertEqual(fetched_reservation.reservation_id, reservation.reservation_id)

    def test_get_reservations_by_user_id(self):
        user_id = self._get_user_id('john_doe')
        movie_id = self._get_movie_id('Inception')
        showtime_id = self._get_showtime_id(movie_id)
        reservation1 = Reservation.create_reservation(user_id, movie_id, showtime_id, 'A1', db=self.test_db)
        reservation2 = Reservation.create_reservation(user_id, movie_id, showtime_id, 'A2', db=self.test_db)
        reservations = Reservation.get_reservations_by_user_id(user_id, db=self.test_db)
        self.assertEqual(len(reservations), 2)
        self.assertEqual(reservations[0].reservation_id, reservation1.reservation_id)
        self.assertEqual(reservations[1].reservation_id, reservation2.reservation_id)

    def _get_user_id(self, username):
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM users WHERE username = ?', (username,))
        user_id = cursor.fetchone()[0]
        conn.close()
        return user_id

    def _get_movie_id(self, title):
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute('SELECT movie_id FROM movies WHERE title = ?', (title,))
        movie_id = cursor.fetchone()[0]
        conn.close()
        return movie_id

    def _get_showtime_id(self, movie_id):
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute('SELECT showtime_id FROM showtimes WHERE movie_id = ?', (movie_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        return None


if __name__ == '__main__':
    unittest.main()
