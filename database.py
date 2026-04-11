import sqlite3
import os
import random
from contextlib import contextmanager

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'app.db')


@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def create_tables():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS connection (
                key TEXT PRIMARY KEY CHECK(length(key) = 20),
                name TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS share (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                connection TEXT NOT NULL,
                share TEXT NOT NULL,
                FOREIGN KEY (connection) REFERENCES connection(key)
            )
        ''')
        
        conn.commit()


def init_database():
    create_tables()


def generate_20_digit_key():
    key = ''.join([str(random.randint(0, 9)) for _ in range(20)])
    return key


def create_connection(key, name):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO connection (key, name) VALUES (?, ?)', (key, name))
        conn.commit()


def key_exists(key):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM connection WHERE key = ?', (key,))
        return cursor.fetchone() is not None


def generate_unique_key():
    while True:
        key = generate_20_digit_key()
        if not key_exists(key):
            return key


def get_connection_name(key):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM connection WHERE key = ?', (key,))
        result = cursor.fetchone()
        return result['name'] if result else None


def save_or_update_share(connection_key, share_data):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM share WHERE connection = ?', (connection_key,))
        existing = cursor.fetchone()
        if existing:
            cursor.execute('UPDATE share SET share = ? WHERE connection = ?', (share_data, connection_key))
        else:
            cursor.execute('INSERT INTO share (connection, share) VALUES (?, ?)', (connection_key, share_data))
        conn.commit()


def get_share_data(connection_key):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT share FROM share WHERE connection = ?', (connection_key,))
        result = cursor.fetchone()
        return result['share'] if result else None
