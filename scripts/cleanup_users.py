import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db.connection import db_cursor


def delete_non_admin_users():
    with db_cursor() as (conn, cur):
        cur.execute("SELECT id, email FROM users WHERE role != 'ADMIN'")
        non_admins = cur.fetchall()
        if not non_admins:
            print("No non-admin users found. Nothing to delete.")
            return

        ids = [row['id'] for row in non_admins]
        emails = [row['email'] for row in non_admins]
        print(f"Deleting {len(ids)} non-admin users: {emails}")

        placeholders = ','.join(['%s'] * len(ids))
        cur.execute(f"DELETE FROM warehouse_events WHERE user_id IN ({placeholders})", ids)
        cur.execute(f"DELETE FROM requests WHERE user_id IN ({placeholders})", ids)
        cur.execute(f"DELETE FROM users WHERE id IN ({placeholders})", ids)
        conn.commit()
        print("Cleanup complete.")

        cur.execute("SELECT id, email FROM users WHERE role='ADMIN'")
        admins = cur.fetchall()
        print("Remaining admin users:", admins)


def main():
    delete_non_admin_users()


if __name__ == "__main__":
    main()
