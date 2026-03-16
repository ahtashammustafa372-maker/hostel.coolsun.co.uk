import sqlite3
import os

db_path = r'd:\Coolsun Hostel\Coolsun Hostel\backend\instance\hostel.db'
if not os.path.exists(db_path):
    # Try the path from app.py
    _BASE_DIR = os.path.abspath(os.path.join(r'd:\Coolsun Hostel\Coolsun Hostel\backend', '..'))
    db_path = os.path.join(_BASE_DIR, 'hostel.db')

print(f"Checking DB at: {db_path}")
if not os.path.exists(db_path):
    print("DB still not found.")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='rooms'")
row = cursor.fetchone()
if row:
    print("--- Rooms Table SQL ---")
    print(row[0])
else:
    print("Rooms table not found in sqlite_master.")

conn.close()
