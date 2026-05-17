import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    try:
        if DATABASE_URL:
            conn = psycopg2.connect(
                DATABASE_URL,
                cursor_factory=RealDictCursor
            )
        else:
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
                cursor_factory=RealDictCursor
            )
        print("Database connected successfully.")
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None

def init_db():
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trucks (
                id SERIAL PRIMARY KEY,
                truck_number VARCHAR(20),
                fuel_efficiency FLOAT,
                is_available BOOLEAN DEFAULT TRUE
            );

            CREATE TABLE IF NOT EXISTS drivers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                phone VARCHAR(20),
                is_available BOOLEAN DEFAULT TRUE
            );

            CREATE TABLE IF NOT EXISTS deliveries (
                id SERIAL PRIMARY KEY,
                origin VARCHAR(255),
                destination VARCHAR(255),
                distance_km FLOAT,
                predicted_time_min FLOAT,
                truck_id INTEGER REFERENCES trucks(id),
                driver_id INTEGER REFERENCES drivers(id),
                status VARCHAR(50),
                delivery_start TIMESTAMP,
                delivery_end TIMESTAMP
            );
        """)
        conn.commit()
        print("Database initialized successfully.")
    except Exception as e:
        print("Database initialization failed:", e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    init_db()
