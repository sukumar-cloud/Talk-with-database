import os
from urllib.parse import quote
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import make_url
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv("DB_URI")
if not DB_URI:
    raise SystemExit("DB_URI not set in environment")

url = make_url(DB_URI)
username = url.username or ""
password = url.password or ""
host = url.host or "127.0.0.1"
port = url.port or 3306
dbname = url.database

if not dbname:
    raise SystemExit("Database name is missing in DB_URI")

# Server-level URI without database to create DB if missing
server_uri = f"mysql+pymysql://{quote(username)}:{quote(password)}@{host}:{port}/"
server_engine = create_engine(server_uri, pool_pre_ping=True)

print(f"Ensuring database exists: {dbname}")
with server_engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{dbname}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))

# Connect to target DB
engine = create_engine(DB_URI, pool_pre_ping=True)

print("Creating tables if not exist...")
with engine.begin() as conn:
    conn.execute(text(
        """
        CREATE TABLE IF NOT EXISTS customers (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(120) UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    ))
    conn.execute(text(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INT PRIMARY KEY AUTO_INCREMENT,
            customer_id INT NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
        """
    ))

print("Seeding sample data (idempotent upserts)...")
with engine.begin() as conn:
    # Insert customers if table empty
    count = conn.execute(text("SELECT COUNT(*) FROM customers")).scalar()
    if count == 0:
        conn.execute(text("INSERT INTO customers (name, email) VALUES (:n,:e)"), [
            {"n": "Alice", "e": "alice@example.com"},
            {"n": "Bob", "e": "bob@example.com"},
            {"n": "Charlie", "e": "charlie@example.com"}
        ])
    # Insert orders if table empty
    count_o = conn.execute(text("SELECT COUNT(*) FROM orders")).scalar()
    if count_o == 0:
        conn.execute(text("INSERT INTO orders (customer_id, amount, status) VALUES (:c,:a,:s)"), [
            {"c": 1, "a": 120.50, "s": "paid"},
            {"c": 1, "a": 75.00, "s": "paid"},
            {"c": 2, "a": 300.00, "s": "shipped"},
            {"c": 3, "a": 45.99, "s": "pending"}
        ])

print("Seed completed.")
