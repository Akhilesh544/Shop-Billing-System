import sqlite3

DATABASE_NAME = "billing.db"

def get_connection():
    return sqlite3.connect(DATABASE_NAME)

def create_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS bills(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT,
        payment_method TEXT,
        total REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS bill_items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bill_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        price REAL,
        subtotal REAL
    )
    """)

    conn.commit()
    conn.close()

if __name__=="__main__":
    create_database()
    print("Database Ready")
