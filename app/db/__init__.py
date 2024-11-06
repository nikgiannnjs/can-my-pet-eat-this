import psycopg2
import os

try:
    connection = psycopg2.connect(
        host = os.getenv("HOST"),
        port = os.getenv("POSTGRESQL_PORT"),
        database = os.getenv("DATABASE"),
        user = os.getenv("POSTGRESQL_USER"),
        password = os.getenv("PASSWORD")
    )

    print("Database connected successfully.")
except psycopg2.Error as e:
    print(f"Error connecting to the db: {e}")
    connection = None
