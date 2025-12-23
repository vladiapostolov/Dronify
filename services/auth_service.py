from werkzeug.security import generate_password_hash, check_password_hash
from db.connection import db_cursor
from models.user import User

def get_user_by_id(user_id: int):
    with db_cursor() as (_, cur):
        cur.execute("""
            SELECT id, email, first_name, last_name, role, is_active
            FROM users WHERE id=%s
        """, (user_id,))
        row = cur.fetchone()
        return User(**row) if row else None

def get_user_by_email(email: str):
    with db_cursor() as (_, cur):
        cur.execute("""
            SELECT id, email, first_name, last_name, role, is_active, password_hash
            FROM users WHERE email=%s
        """, (email,))
        return cur.fetchone()

def register_user(first_name, last_name, email, password, role="BASIC_USER"):
    pwd = generate_password_hash(password)
    with db_cursor() as (conn, cur):
        cur.execute("""
            INSERT INTO users (first_name, last_name, email, password_hash, role)
            VALUES (%s,%s,%s,%s,%s)
        """, (first_name, last_name, email, pwd, role))
        conn.commit()
        return cur.lastrowid

def authenticate(email: str, password: str):
    row = get_user_by_email(email)
    if not row:
        return None
    if not row.get("is_active", 1):
        return None
    if not check_password_hash(row["password_hash"], password):
        return None
    return User(
        id=row["id"],
        email=row["email"],
        first_name=row["first_name"],
        last_name=row["last_name"],
        role=row["role"],
        is_active=bool(row["is_active"])
    )
