from contextlib import contextmanager
import mysql.connector
from config import Config

def get_db():
    return mysql.connector.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        autocommit=False
    )

@contextmanager
def db_cursor(dict_cursor=True):
    conn = get_db()
    cur = conn.cursor(dictionary=dict_cursor)
    try:
        yield conn, cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()
