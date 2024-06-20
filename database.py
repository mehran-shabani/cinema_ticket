import sqlite3


def create_tables():
    conn = sqlite3.connect('cinema.db')
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

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cinemas (
        cinema_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        rating REAL NOT NULL DEFAULT 0,
        cinema_id INTEGER NOT NULL,
        FOREIGN KEY (cinema_id) REFERENCES cinemas (cinema_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS showtimes (
        showtime_id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER NOT NULL,
        showtime TEXT NOT NULL,
        FOREIGN KEY (movie_id) REFERENCES movies (movie_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservations (
        reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        movie_id INTEGER NOT NULL,
        showtime_id INTEGER NOT NULL,
        seat_number TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (movie_id) REFERENCES movies (movie_id),
        FOREIGN KEY (showtime_id) REFERENCES showtimes (showtime_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        review_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        movie_id INTEGER NOT NULL,
        rating INTEGER NOT NULL,
        comment TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (movie_id) REFERENCES movies (movie_id)
    )
    ''')

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
