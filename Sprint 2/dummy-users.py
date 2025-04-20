import os
import sqlite3
import random
import bcrypt

# Resolve DB next to this script file
HERE    = os.path.dirname(__file__)
DB_PATH = os.path.join(HERE, 'users.db')

def make_hash(pw):
    return bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt()).decode('utf8')

conn = sqlite3.connect(DB_PATH)
c    = conn.cursor()

for i in range(1, 51):
    username = f'user{i:02d}'
    email    = f'user{i:02d}@example.com'
    password = make_hash('password123')        # everyone uses the same dummy password
    points   = random.randint(0, 500)         # give each user 0–5000 points

    try:
        c.execute("""
          INSERT INTO user (username, email, password, points)
          VALUES (?, ?, ?, ?)
        """, (username, email, password, points))
    except sqlite3.IntegrityError:
        # skip if already exists
        pass

conn.commit()
conn.close()
print("Inserted up to 50 dummy users with random points.")
