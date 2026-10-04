import sqlite3
from src.config import DATABASE_PATH


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def create_products_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL,
            discount_percentage REAL NOT NULL,
            rating REAL NOT NULL
        )
        """)
    conn.commit()


def upsert_products(conn, products):
    cursor = conn.cursor()
    cursor.executemany(
        """
        INSERT INTO products (id, title, category, price, discount_percentage, rating)
        VALUES (:id, :title, :category, :price, :discount_percentage, :rating)
        ON CONFLICT(id) DO UPDATE SET
            title = excluded.title,
            category = excluded.category,
            price = excluded.price,
            discount_percentage = excluded.discount_percentage,
            rating = excluded.rating
        """,
        products,
    )
    conn.commit()
