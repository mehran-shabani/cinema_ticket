import unittest
import sqlite3
import os
import uuid
from review import Review


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
    CREATE TABLE IF NOT EXISTS reviews (
        review_id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        movie_id TEXT NOT NULL,
        rating INTEGER NOT NULL,
        comment TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (movie_id) REFERENCES movies (movie_id)
    )
    ''')
    conn.commit()
    conn.close()


class TestReview(unittest.TestCase):
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
        cursor.execute('DELETE FROM reviews')
        cursor.execute('DELETE FROM movies')
        cursor.execute('DELETE FROM cinemas')
        cursor.execute('DELETE FROM users')

        # اضافه کردن داده‌های نمونه برای کاربران، سینماها، و فیلم‌ها
        user_id = str(uuid.uuid4())
        cinema_id = str(uuid.uuid4())
        movie_id = str(uuid.uuid4())

        cursor.execute(
            'INSERT INTO users (user_id, username, email, phone_number, password, birth_date, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (user_id, 'john_doe', 'john@example.com', 1234567890, 'password', '1990-01-01', '2024-01-01'))
        cursor.execute('INSERT INTO cinemas (cinema_id, name) VALUES (?, ?)', (cinema_id, 'Cinema One'))
        cursor.execute('INSERT INTO movies (movie_id, title, cinema_id) VALUES (?, ?, ?)',
                       (movie_id, 'Inception', cinema_id))
        conn.commit()
        conn.close()

        self.user_id = user_id
        self.movie_id = movie_id

    def test_create_review(self):
        review = Review.create_review(self.user_id, self.movie_id, 5, 'Great movie!', db=self.test_db)
        self.assertIsNotNone(review.review_id)
        self.assertEqual(review.user_id, self.user_id)
        self.assertEqual(review.movie_id, self.movie_id)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Great movie!')

    def test_get_review_by_id(self):
        review = Review.create_review(self.user_id, self.movie_id, 5, 'Great movie!', db=self.test_db)
        fetched_review = Review.get_review_by_id(review.review_id, db=self.test_db)
        self.assertIsNotNone(fetched_review)
        self.assertEqual(fetched_review.review_id, review.review_id)

    def test_get_reviews_by_movie_id(self):
        review1 = Review.create_review(self.user_id, self.movie_id, 5, 'Great movie!', db=self.test_db)
        review2 = Review.create_review(self.user_id, self.movie_id, 4, 'Good movie.', db=self.test_db)
        reviews = Review.get_reviews_by_movie_id(self.movie_id, db=self.test_db)
        self.assertEqual(len(reviews), 2)
        self.assertEqual(reviews[0].review_id, review1.review_id)
        self.assertEqual(reviews[1].review_id, review2.review_id)


if __name__ == '__main__':
    unittest.main()
