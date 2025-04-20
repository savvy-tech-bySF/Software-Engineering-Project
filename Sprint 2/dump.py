import os
import sqlite3

# Resolve DB next to this script file
HERE    = os.path.dirname(__file__)
DB_PATH = os.path.join(HERE, 'users.db')

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("---- USERS ----")
for row in cursor.execute("SELECT * FROM user"):
    print(dict(row))

print("\n---- PRs ----")
for row in cursor.execute("SELECT * FROM pr"):
    print(dict(row))

conn.close()
