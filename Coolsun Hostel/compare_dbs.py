import sqlite3
import os

db_root = r'd:\Coolsun Hostel\Coolsun Hostel\hostel.db'
db_instance = r'd:\Coolsun Hostel\Coolsun Hostel\backend\instance\hostel.db'

def check_db(path, name):
    print(f"\n--- Checking {name} ({path}) ---")
    if not os.path.exists(path):
        print("Not found.")
        return
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, number FROM rooms")
        rooms = cursor.fetchall()
        print(f"Rooms: {rooms}")
        
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='rooms'")
        print(f"SQL: {cursor.fetchone()[0]}")
    except Exception as e:
        print(f"Error: {e}")
    conn.close()

check_db(db_root, "Root DB")
check_db(db_instance, "Instance DB")
