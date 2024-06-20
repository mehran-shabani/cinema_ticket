import uuid
import sqlite3

class Review:
    def __init__(self, review_id, user_id, movie_id, rating, comment):
        self.review_id = review_id
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating
        self.comment = comment
        self.replies = []

    @staticmethod
    def create_review(user_id, movie_id, rating, comment, db='cinema.db'):
        review_id = str(uuid.uuid4())
        review = Review(review_id, user_id, movie_id, rating, comment)
        review.save_to_db(db)
        return review

    def save_to_db(self, db='cinema.db'):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO reviews (review_id, user_id, movie_id, rating, comment)
        VALUES (?, ?, ?, ?, ?)
        ''', (self.review_id, self.user_id, self.movie_id, self.rating, self.comment))
        conn.commit()
        conn.close()

    @staticmethod
    def get_review_by_id(review_id, db='cinema.db'):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM reviews WHERE review_id = ?
        ''', (review_id,))
        review_data = cursor.fetchone()
        conn.close()
        if review_data:
            return Review(*review_data)
        return None

    @staticmethod
    def get_reviews_by_movie_id(movie_id, db='cinema.db'):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM reviews WHERE movie_id = ?
        ''', (movie_id,))
        reviews_data = cursor.fetchall()
        conn.close()
        return [Review(*review_data) for review_data in reviews_data]

    def add_reply(self, reply):
        self.replies.append(reply)
        # Here you might want to save replies to the database as well, but it's not implemented
