import os
import sqlite3


class Database:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.base_dir, '../..', 'data')
        self.db_path = os.path.join(self.data_dir, 'db.sqlite3')

        os.makedirs(self.data_dir, exist_ok=True)
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS listings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    listing_id TEXT UNIQUE,
                    url TEXT,
                    price REAL,
                    address TEXT,
                    neighborhood TEXT
                )
            """)
            conn.commit()

    def get_existing_ids(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT listing_id FROM listings')
            return set(row[0] for row in cursor.fetchall())

    def get_listings_sorted(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM listings ORDER BY created_at DESC')
            return [dict(row) for row in cursor.fetchall()]

    def insert_new_listing(self, listing):
        columns = ', '.join(listing.keys())
        placeholders = ', '.join('?' * len(listing))
        sql = f'INSERT OR IGNORE INTO listings ({columns}) VALUES ({placeholders})'

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, tuple(listing.values()))
            conn.commit()
