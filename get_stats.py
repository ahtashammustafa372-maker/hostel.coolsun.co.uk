import sqlite3
import os

db_path = r'd:\Coolsun Hostel\Coolsun Hostel\backend\instance\hostel.db'
if not os.path.exists(db_path):
    print(f"DB not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("--- All Tenants ---")
cursor.execute("SELECT id, name FROM tenants WHERE deleted_at IS NULL")
tenants = cursor.fetchall()
for t in tenants:
    print(t)

print("\n--- Paid Totals By Type (This Month) ---")
# Let's assume this month starts 2026-03-01
cursor.execute("""
    SELECT type, SUM(amount) 
    FROM ledger 
    WHERE status='PAID' AND timestamp >= '2026-03-01' AND deleted_at IS NULL
    GROUP BY type
""")
totals = cursor.fetchall()
for t in totals:
    print(t)

conn.close()
