import unittest
import sqlite3
import os
from user import User


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
    conn.commit()
    conn.close()


class TestUser(unittest.TestCase):
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
        cursor.execute('DELETE FROM users')
        conn.commit()
        conn.close()

    def test_create_user(self):
        user = User.create_user('john_doe', 'john@example.com', 'password123', '1990-01-01', db=self.test_db)
        self.assertIsNotNone(user.user_id)
        self.assertEqual(user.username, 'john_doe')
        self.assertEqual(user.email, 'john@example.com')
        self.assertNotEqual(user.password, 'password123')  # Password should be hashed
        self.assertEqual(user.wallet_balance, 0.0)
        self.assertEqual(user.subscription, 'Bronze')

    def test_get_user_by_username(self):
        user = User.create_user('john_doe', 'john@example.com', 'password123', '1990-01-01', db=self.test_db)
        fetched_user = User.get_user_by_username('john_doe', db=self.test_db)
        self.assertIsNotNone(fetched_user)
        self.assertEqual(fetched_user.username, 'john_doe')
        self.assertEqual(fetched_user.email, 'john@example.com')

    def test_get_user_by_id(self):
        user = User.create_user('john_doe', 'john@example.com', 'password123', '1990-01-01', db=self.test_db)
        fetched_user = User.get_user_by_id(user.user_id, db=self.test_db)
        self.assertIsNotNone(fetched_user)
        self.assertEqual(fetched_user.user_id, user.user_id)
        self.assertEqual(fetched_user.username, 'john_doe')


if __name__ == '__main__':
    unittest.main()
