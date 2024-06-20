import uuid
import sqlite3

class Cinema:
    def __init__(self, cinema_id, name):
        self.cinema_id = cinema_id
        self.name = name
        self.movies = []

    @staticmethod
    def create_cinema(name, db='cinema.db'):
        cinema_id = str(uuid.uuid4())
        cinema = Cinema(cinema_id, name)
        cinema.save_to_db(db)
        return cinema

    def save_to_db(self, db='cinema.db'):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO cinemas (cinema_id, name)
        VALUES (?, ?)
        ''', (self.cinema_id, self.name))
        conn.commit()
        conn.close()

    @staticmethod
    def get_cinema_by_name(name, db='cinema.db'):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM cinemas WHERE name = ?
        ''', (name,))
        cinema_data = cursor.fetchone()
        conn.close()
        if cinema_data:
            return Cinema(*cinema_data)
        return None

    @staticmethod
    def get_cinema_by_id(cinema_id, db='cinema.db'):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM cinemas WHERE cinema_id = ?
        ''', (cinema_id,))
        cinema_data = cursor.fetchone()
        conn.close()
        if cinema_data:
            return Cinema(*cinema_data)
        return None
