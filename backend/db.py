import os
import psycopg2
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)
DATABASE_URL = os.getenv('DATABASE_URL')

def get_db_connection():
    try:
        return psycopg2.connect(DATABASE_URL)
    except Exception as e:
        print(f"ERROR al conectar a DB: {e}")
        return None

def release_db_connection(conn):
    if conn:
        conn.close()