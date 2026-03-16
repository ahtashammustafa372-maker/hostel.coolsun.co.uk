import sqlite3

db_path = r'd:\Coolsun Hostel\Coolsun Hostel\hostel.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Find duplicate numbers
cursor.execute("SELECT number, COUNT(*) FROM rooms GROUP BY number HAVING COUNT(*) > 1")
duplicates = cursor.fetchall()

for number, count in duplicates:
    print(f"Cleaning up Room {number} ({count} entries)...")
    # Keep the first ID, delete others
    cursor.execute("SELECT id FROM rooms WHERE number = ? ORDER BY id ASC", (number,))
    ids = [row[0] for row in cursor.fetchall()]
    keep_id = ids[0]
    delete_ids = ids[1:]
    
    for rid in delete_ids:
        cursor.execute("DELETE FROM rooms WHERE id = ?", (rid,))

conn.commit()
conn.close()
print("Cleanup complete.")
