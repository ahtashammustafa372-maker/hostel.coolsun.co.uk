import sqlite3
import os

db_root = r'd:\Coolsun Hostel\Coolsun Hostel\hostel.db'
db_instance_bak = r'd:\Coolsun Hostel\Coolsun Hostel\backend\instance\hostel.db.bak'

def check_tenants(path, name):
    print(f"\n--- Checking {name} ({path}) ---")
    if not os.path.exists(path):
        print("Not found.")
        return
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, room_id FROM tenants")
        tenants = cursor.fetchall()
        print(f"Tenants: {tenants}")
        
        cursor.execute("SELECT id, amount, type, status FROM ledger")
        ledger = cursor.fetchall()
        print(f"Ledger entries count: {len(ledger)}")
    except Exception as e:
        print(f"Error: {e}")
    conn.close()

check_tenants(db_root, "Root DB")
check_tenants(db_instance_bak, "Instance DB (Bak)")
