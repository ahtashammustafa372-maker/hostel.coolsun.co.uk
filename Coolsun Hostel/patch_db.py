import sqlite3

conn = sqlite3.connect(r'D:\Coolsun Hostel\Coolsun Hostel\backend\instance\hostel.db')
cursor = conn.cursor()
try:
    cursor.execute("ALTER TABLE tenants ADD COLUMN internet_opt_in BOOLEAN DEFAULT 1")
    conn.commit()
    print("Added internet_opt_in to tenants table successfully.")
except sqlite3.OperationalError as e:
    print(f"Skipping Add internet_opt_in: {e}")

try:
    cursor.execute("ALTER TABLE rooms ADD COLUMN base_rent DECIMAL(10, 2) DEFAULT 10000.00")
    conn.commit()
    print("Added base_rent to rooms table successfully.")
except sqlite3.OperationalError as e:
    print(f"Skipping Add base_rent: {e}")

try:
    cursor.execute("UPDATE rooms SET type='Medium' WHERE type='Shared'")
    conn.commit()
    print("Patched rooms table successfully.")
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
