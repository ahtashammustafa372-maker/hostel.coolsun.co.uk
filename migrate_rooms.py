import sqlite3
import os

db_path = r'd:\Coolsun Hostel\Coolsun Hostel\hostel.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # SQLite doesn't support ALTER TABLE for UNIQUE directly easily without recreating table,
    # but we can add a UNIQUE INDEX.
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_room_number ON rooms(number)")
    conn.commit()
    print("Migration successful: added unique index on rooms(number).")
except Exception as e:
    print(f"Migration failed: {e}")

conn.close()
