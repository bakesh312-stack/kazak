import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    bonus INTEGER DEFAULT 6,
    invited_by INTEGER,
    referrals INTEGER DEFAULT 0
)
""")
conn.commit()

def add_user(user_id, invited_by=None):
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO users (user_id, invited_by) VALUES (?,?)",
            (user_id, invited_by)
        )
        conn.commit()
        return True
    return False

def get_bonus(user_id):
    cursor.execute("SELECT bonus FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone()[0]

def update_bonus(user_id, amount):
    cursor.execute(
        "UPDATE users SET bonus = bonus + ? WHERE user_id=?",
        (amount, user_id)
    )
    conn.commit()                   (inviter_id,))
    conn.commit()
