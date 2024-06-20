import uuid
import sqlite3


class Showtime:
    def __init__(self, showtime_id, movie_id, showtime):
        self.showtime_id = showtime_id
        self.movie_id = movie_id
        self.showtime = showtime

    @staticmethod
    def create_showtime(movie_id, showtime_str, db='cinema.db'):
        showtime_id = str(uuid.uuid4())
        showtime = Showtime(showtime_id, movie_id, showtime_str)
        showtime.save_to_db(db)
        return showtime

    def save_to_db(self, db='cinema.db'):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO showtimes (showtime_id, movie_id, showtime)
        VALUES (?, ?, ?)
        ''', (self.showtime_id, self.movie_id, self.showtime))
        conn.commit()
        conn.close()

    @staticmethod
    def get_showtime_by_id(showtime_id, db='cinema.db'):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM showtimes WHERE showtime_id = ?
        ''', (showtime_id,))
        showtime_data = cursor.fetchone()
        conn.close()
        if showtime_data:
            return Showtime(*showtime_data)
        return None
