import uuid
import sqlite3

class Reservation:
    def __init__(self, reservation_id, user_id, movie_id, showtime_id, seat_number, status):
        self.reservation_id = reservation_id
        self.user_id = user_id
        self.movie_id = movie_id
        self.showtime_id = showtime_id
        self.seat_number = seat_number
        self.status = status

    @staticmethod
    def create_reservation(user_id, movie_id, showtime_id, seat_number, db='cinema.db'):
        reservation_id = str(uuid.uuid4())
        reservation = Reservation(reservation_id, user_id, movie_id, showtime_id, seat_number, "reserved")
        reservation.save_to_db(db)
        return reservation

    def save_to_db(self, db='cinema.db'):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO reservations (reservation_id, user_id, movie_id, showtime_id, seat_number, status)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.reservation_id, self.user_id, self.movie_id, self.showtime_id, self.seat_number, self.status))
        conn.commit()
        conn.close()

    @staticmethod
    def get_reservation_by_id(reservation_id, db='cinema.db'):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM reservations WHERE reservation_id = ?
        ''', (reservation_id,))
        reservation_data = cursor.fetchone()
        conn.close()
        if reservation_data:
            return Reservation(*reservation_data)
        return None

    @staticmethod
    def get_reservations_by_user_id(user_id, db='cinema.db'):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM reservations WHERE user_id = ?
        ''', (user_id,))
        reservations_data = cursor.fetchall()
        conn.close()
        return [Reservation(*reservation_data) for reservation_data in reservations_data]
