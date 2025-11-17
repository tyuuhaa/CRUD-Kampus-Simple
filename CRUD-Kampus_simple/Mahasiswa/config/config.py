# config.py
import psycopg2
from psycopg2.extras import RealDictCursor

def get_conn():
    return psycopg2.connect(
        dbname="db_mahasiswa",
        user="postgres",
        password="password_anda",
        host="localhost",
        port=5432
    )
