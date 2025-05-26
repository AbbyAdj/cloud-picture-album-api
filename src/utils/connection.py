import os
from dotenv import load_dotenv
from pg8000.native import Connection

load_dotenv(override=True)


def connect_to_db():
    PG_USER = os.getenv("DB_USER", default="postgres")
    PG_HOST = os.getenv("DB_HOST", default="localhost")
    PG_DATABASE = os.getenv("DB_DATABASE", default="postgres")
    PG_PASSWORD = os.getenv("DB_PASSWORD")

    # print(PG_USER, "host:", PG_HOST, PG_DATABASE, PG_PASSWORD)
    conn = Connection(
        user=PG_USER, host=PG_HOST, database=PG_DATABASE, password=PG_PASSWORD, ssl_context=True
    )

    return conn


def close_db_connection(conn):
    conn.close()
