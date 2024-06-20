import unittest
import sqlite3
import os
from cinema import Cinema

def create_tables(db_name='test_cinema.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cinemas (
        cinema_id TEXT PRIMARY KEY,
        name TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

class TestCinema(unittest.TestCase):
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
        cursor.execute('DELETE FROM cinemas')
        conn.commit()
        conn.close()

    def test_create_cinema(self):
        cinema = Cinema.create_cinema('Cinema One', db=self.test_db)
        self.assertIsNotNone(cinema.cinema_id)
        self.assertEqual(cinema.name, 'Cinema One')

    def test_get_cinema_by_name(self):
        cinema = Cinema.create_cinema('Cinema One', db=self.test_db)
        fetched_cinema = Cinema.get_cinema_by_name('Cinema One', db=self.test_db)
        self.assertIsNotNone(fetched_cinema)
        self.assertEqual(fetched_cinema.name, 'Cinema One')

    def test_get_cinema_by_id(self):
        cinema = Cinema.create_cinema('Cinema One', db=self.test_db)
        fetched_cinema = Cinema.get_cinema_by_id(cinema.cinema_id, db=self.test_db)
        self.assertIsNotNone(fetched_cinema)
        self.assertEqual(fetched_cinema.cinema_id, cinema.cinema_id)
        self.assertEqual(fetched_cinema.name, 'Cinema One')

if __name__ == '__main__':
    unittest.main()
