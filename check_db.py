import sqlite3
import os

db_path = r'd:\Coolsun Hostel\Coolsun Hostel\backend\instance\hostel.db'
if not os.path.exists(db_path):
    print(f"DB not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("--- Ledger Table Columns ---")
cursor.execute("PRAGMA table_info(ledger)")
columns = cursor.fetchall()
for col in columns:
    print(col)

print("\n--- Tenants (Ahtasham / Junaid) ---")
cursor.execute("SELECT id, name FROM tenants WHERE name LIKE '%Ahtasham%' OR name LIKE '%Junaid%'")
tenants = cursor.fetchall()
for t in tenants:
    print(t)

print("\n--- Recent Ledger Entries ---")
cursor.execute("SELECT id, tenant_id, amount, type, status, timestamp, description FROM ledger ORDER BY timestamp DESC LIMIT 10")
entries = cursor.fetchall()
for e in entries:
    print(e)

conn.close()
