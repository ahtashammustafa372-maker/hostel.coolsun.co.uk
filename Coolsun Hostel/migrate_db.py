import sqlite3
import os

db_path = r'd:\Coolsun Hostel\Coolsun Hostel\backend\instance\hostel.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE ledger ADD COLUMN payment_method VARCHAR(20) DEFAULT 'Cash'")
    conn.commit()
    print("Migration successful: added payment_method to ledger.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e).lower():
        print("Column payment_method already exists.")
    else:
        print(f"Migration failed: {e}")

conn.close()
