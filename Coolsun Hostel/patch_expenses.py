import sqlite3
import os

for db_path in ['instance/hostel.db', 'hostel.db']:
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("UPDATE expenses SET category='Repairs' WHERE category='Maintenance'")
            print(f"Updated {cur.rowcount} rows in {db_path}")
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Failed to update {db_path}: {e}")
            
