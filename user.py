import uuid
import hashlib
import datetime
import sqlite3

class User:
    def __init__(self, user_id, username, email, phone_number, password, birth_date, registration_date, wallet_balance, subscription, last_login=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.birth_date = birth_date
        self.registration_date = registration_date
        self.wallet_balance = wallet_balance
        self.subscription = subscription
        self.last_login = last_login

    @staticmethod
    def create_user(username, email, password, birth_date, phone_number=None, db='cinema.db'):
        user_id = str(uuid.uuid4())
        hashed_password = User.hash_password(password)
        registration_date = datetime.datetime.now().isoformat()
        user = User(user_id, username, email, phone_number, hashed_password, birth_date, registration_date, 0.0, "Bronze")
        user.save_to_db(db)
        return user

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def save_to_db(self, db='cinema.db'):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO users (user_id, username, email, phone_number, password, birth_date, registration_date, wallet_balance, subscription, last_login)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.user_id, self.username, self.email, self.phone_number, self.password, self.birth_date, self.registration_date, self.wallet_balance, self.subscription, self.last_login))
        conn.commit()
        conn.close()

    @staticmethod
    def get_user_by_username(username, db='cinema.db'):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM users WHERE username = ?
        ''', (username,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            return User(*user_data)
        return None

    @staticmethod
    def get_user_by_id(user_id, db='cinema.db'):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM users WHERE user_id = ?
        ''', (user_id,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            return User(*user_data)
        return None
