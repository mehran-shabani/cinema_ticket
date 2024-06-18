import uuid
import re
import hashlib
import datetime
import sqlite3

class User:
    def __init__(self, username, email, password, birth_date, phone_number=None):
        self.user_id = str(uuid.uuid4())
        self.username = self.validate_username(username)
        self.email = self.validate_email(email)
        self.phone_number = self.validate_phone_number(phone_number)
        self.password = self.hash_password(password)
        self.birth_date = birth_date
        self.registration_date = datetime.datetime.now()
        self.last_login = None
        self.wallet_balance = 0.0
        self.subscription = "Bronze"
        self.save_to_db()

    def validate_username(self, username):
        if len(username) > 100 or not re.match("^[A-Za-z0-9]*$", username):
            raise ValueError("نام کاربری نامعتبر است")
        return username

    def validate_email(self, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("فرمت ایمیل نامعتبر است")
        return email

    def validate_phone_number(self, phone_number):
        if phone_number and not re.match(r"^\+?[1-9]\d{1,14}$", phone_number):
            raise ValueError("فرمت شماره تلفن نامعتبر است")
        return phone_number

    def hash_password(self, password):
        if len(password) < 8 or not re.match(r".*[A-Z].*[a-z].*[0-9].*[@#&$]", password):
            raise ValueError("گذرواژه باید حداقل ۸ کاراکتر و شامل حروف بزرگ، کوچک، عدد و کاراکترهای خاص باشد")
        return hashlib.sha256(password.encode()).hexdigest()

    def save_to_db(self):
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO users (user_id, username, email, phone_number, password, birth_date, registration_date, wallet_balance, subscription)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.user_id, self.username, self.email, self.phone_number, self.password, self.birth_date, self.registration_date, self.wallet_balance, self.subscription))
        conn.commit()
        conn.close()

    def update_profile(self, new_email=None, new_phone_number=None):
        if new_email:
            self.email = self.validate_email(new_email)
        if new_phone_number:
            self.phone_number = self.validate_phone_number(new_phone_number)
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE users
        SET email = ?, phone_number = ?
        WHERE user_id = ?
        ''', (self.email, self.phone_number, self.user_id))
        conn.commit()
        conn.close()

    def change_password(self, old_password, new_password, confirm_new_password):
        if self.hash_password(old_password) != self.password:
            raise ValueError("گذرواژه قدیمی اشتباه است")
        if new_password != confirm_new_password:
            raise ValueError("گذرواژه‌های جدید مطابقت ندارند")
        self.password = self.hash_password(new_password)
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE users
        SET password = ?
        WHERE user_id = ?
        ''', (self.password, self.user_id))
        conn.commit()
        conn.close()

    def login(self):
        self.last_login = datetime.datetime.now()
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE users
        SET last_login = ?
        WHERE user_id = ?
        ''', (self.last_login, self.user_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_user(username):
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM users WHERE username = ?
        ''', (username,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            return User(*user_data[1:])
        return None
