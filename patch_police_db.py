import sqlite3

conn = sqlite3.connect(r'D:\Coolsun Hostel\Coolsun Hostel\backend\instance\hostel.db')
cursor = conn.cursor()

new_columns = [
    "father_name VARCHAR(100)",
    "permanent_address TEXT",
    "police_station VARCHAR(100)"
]

for col in new_columns:
    try:
        cursor.execute(f"ALTER TABLE tenants ADD COLUMN {col}")
        print(f"Added {col} successfully.")
    except sqlite3.OperationalError as e:
        print(f"Skipping {col}: {e}")

conn.commit()
conn.close()
print("Database patch completed.")
