import uuid
import datetime
import sqlite3

class Reservation:
    def __init__(self, user_id, movie_id, showtime_id, seat_number):
        self.reservation_id = str(uuid.uuid4())
        self.user_id = user_id
        self.movie_id = movie_id
        self.showtime_id = showtime_id
        self.seat_number = seat_number
        self.status = "reserved"
        self.save_to_db()

    def save_to_db(self):
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO reservations (reservation_id, user_id, movie_id, showtime_id, seat_number, status)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.reservation_id, self.user_id, self.movie_id, self.showtime_id, self.seat_number, self.status))
        conn.commit()
        conn.close()

    def cancel_reservation(self, current_time):
        showtime_datetime = datetime.datetime.strptime(self.showtime_id, "%Y-%m-%d %H:%M")
        time_diff = showtime_datetime - current_time
        if time_diff.total_seconds() > 3600:
            self.status = "canceled"
            self.update_status()
            return "Full refund"
        elif time_diff.total_seconds() > 0:
            self.status = "canceled"
            self.update_status()
            return "18% deduction"
        else:
            return "No refund"

    def update_status(self):
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE reservations
        SET status = ?
        WHERE reservation_id = ?
        ''', (self.status, self.reservation_id))
        conn.commit()
        conn.close()
