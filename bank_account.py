import hashlib
import sqlite3


class BankAccount:
    def __init__(self, user_id, account_number, password, cvv2, initial_balance=0):
        self.account_number = account_number
        self.user_id = user_id
        self.password = self.hash_password(password)
        self.cvv2 = cvv2
        self.balance = initial_balance
        self.save_to_db()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def save_to_db(self):
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO bank_accounts (account_number, user_id, password, cvv2, balance)
        VALUES (?, ?, ?, ?, ?)
        ''', (self.account_number, self.user_id, self.password, self.cvv2, self.balance))
        conn.commit()
        conn.close()

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("مبلغ واریز باید مثبت باشد")
        self.balance += amount
        self.update_balance()

    def withdraw(self, amount, password, cvv2):
        if amount <= 0:
            raise ValueError("مبلغ برداشت باید مثبت باشد")
        if self.hash_password(password) != self.password:
            raise ValueError("گذرواژه اشتباه است")
        if self.cvv2 != cvv2:
            raise ValueError("CVV2 اشتباه است")
        if amount > self.balance:
            raise ValueError("موجودی کافی نیست")
        self.balance -= amount
        self.update_balance()

    def transfer(self, amount, target_account, password, cvv2):
        if amount <= 0:
            raise ValueError("مبلغ انتقال باید مثبت باشد")
        if self.hash_password(password) != self.password:
            raise ValueError("گذرواژه اشتباه است")
        if self.cvv2 != cvv2:
            raise ValueError("CVV2 اشتباه است")
        if amount > self.balance:
            raise ValueError("موجودی کافی نیست")
        self.balance -= amount
        self.update_balance()
        target_account.deposit(amount)

    def update_balance(self):
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE bank_accounts
        SET balance = ?
        WHERE account_number = ?
        ''', (self.balance, self.account_number))
        conn.commit()
        conn.close()
