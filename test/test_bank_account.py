import unittest
import sqlite3
import os
from bank_account import BankAccount


def create_tables(db_name='test_cinema.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone_number INTEGER UNIQUE,
        password TEXT NOT NULL,
        birth_date TEXT NOT NULL,
        registration_date TEXT NOT NULL,
        last_login TEXT,
        wallet_balance REAL NOT NULL DEFAULT 0.0,
        subscription TEXT NOT NULL DEFAULT 'Bronze'
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bank_accounts (
        account_number TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL,
        password TEXT NOT NULL,
        cvv2 TEXT NOT NULL,
        balance REAL NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')
    conn.commit()
    conn.close()


class TestBankAccount(unittest.TestCase):
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
        cursor.execute('DELETE FROM bank_accounts')
        conn.commit()
        conn.close()
        self.account = BankAccount('user123', 'acc123', 'pass123', '123', initial_balance=1000, db=self.test_db)

    def test_account_creation(self):
        self.assertEqual(self.account.user_id, 'user123')
        self.assertEqual(self.account.account_number, 'acc123')
        self.assertEqual(self.account.cvv2, '123')
        self.assertEqual(self.account.balance, 1000)
        self.assertNotEqual(self.account.password, 'pass123')  # Password should be hashed

    def test_deposit(self):
        self.account.deposit(500)
        self.assertEqual(self.account.balance, 1500)

    def test_withdraw(self):
        self.account.withdraw(300, 'pass123', '123')
        self.assertEqual(self.account.balance, 700)

    def test_withdraw_wrong_password(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(300, 'wrongpass', '123')

    def test_withdraw_wrong_cvv2(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(300, 'pass123', '999')

    def test_transfer(self):
        target_account = BankAccount('user456', 'acc456', 'pass456', '456', initial_balance=500, db=self.test_db)
        self.account.transfer(200, target_account, 'pass123', '123')
        self.assertEqual(self.account.balance, 800)
        self.assertEqual(target_account.balance, 700)

    def test_transfer_insufficient_funds(self):
        target_account = BankAccount('user456', 'acc456', 'pass456', '456', initial_balance=500, db=self.test_db)
        with self.assertRaises(ValueError):
            self.account.transfer(2000, target_account, 'pass123', '123')


if __name__ == '__main__':
    unittest.main()
