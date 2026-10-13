import sqlite3
from contextlib import closing


def get_connection(db_path: str) -> sqlite3.Connection:
    """Abre uma conexão com o banco SQLite."""
    return sqlite3.connect(db_path)


def create_products_table(conn):
    """Cria a tabela de produtos no banco de dados, caso ela ainda não exista."""
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
    """Insere ou atualiza (upsert) uma lista de produtos no banco de dados."""
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


def load_to_db(valid_products: list[dict], db_path: str) -> None:
    """Orquestra o processo de salvamento dos produtos no banco de dados."""
    with closing(get_connection(db_path)) as conn:
        create_products_table(conn)
        upsert_products(conn, valid_products)
