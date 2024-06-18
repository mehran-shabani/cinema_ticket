import uuid
import sqlite3

class Review:
    def __init__(self, user_id, movie_id, rating, comment):
        self.review_id = str(uuid.uuid4())
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating
        self.comment = comment
        self.save_to_db()
        self.replies = []

    def save_to_db(self):
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO reviews (review_id, user_id, movie_id, rating, comment)
        VALUES (?, ?, ?, ?, ?)
        ''', (self.review_id, self.user_id, self.movie_id, self.rating, self.comment))
        conn.commit()
        conn.close()

    def add_reply(self, reply):
        self.replies.append(reply)
