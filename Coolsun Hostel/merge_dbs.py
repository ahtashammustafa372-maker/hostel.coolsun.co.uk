import sqlite3
import os

db_root = r'd:\Coolsun Hostel\Coolsun Hostel\hostel.db'
db_instance = r'd:\Coolsun Hostel\Coolsun Hostel\backend\instance\hostel.db'

print(f"Merging {db_instance} into {db_root}...")

conn_root = sqlite3.connect(db_root)
cursor_root = conn_root.cursor()

conn_inst = sqlite3.connect(db_instance)
cursor_inst = conn_inst.cursor()

# Get all rooms from instance DB
cursor_inst.execute("SELECT floor, number, type, capacity, base_rent FROM rooms")
rooms_inst = cursor_inst.fetchall()

# Get existing room numbers in root DB
cursor_root.execute("SELECT number FROM rooms")
existing_numbers = [row[0] for row in cursor_root.fetchall()]

merged_count = 0
for floor, number, rtype, capacity, base_rent in rooms_inst:
    if number not in existing_numbers:
        print(f"Merging Room {number}...")
        cursor_root.execute("""
            INSERT INTO rooms (floor, number, type, capacity, base_rent)
            VALUES (?, ?, ?, ?, ?)
        """, (floor, number, rtype, capacity, base_rent))
        merged_count += 1

conn_root.commit()
conn_root.close()
conn_inst.close()

print(f"Successfully merged {merged_count} rooms.")

# Now delete the instance DB to prevent confusion
try:
    # os.remove(db_instance) # Wait, maybe rename first for safety
    os.rename(db_instance, db_instance + ".bak")
    print(f"Renamed {db_instance} to .bak")
except Exception as e:
    print(f"Could not rename instance DB: {e}")
