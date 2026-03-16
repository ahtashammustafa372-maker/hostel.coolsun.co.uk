import sqlite3
import os

db_root = r'd:\Coolsun Hostel\Coolsun Hostel\hostel.db'
db_instance_bak = r'd:\Coolsun Hostel\Coolsun Hostel\backend\instance\hostel.db.bak'

print(f"Opening DBs...")
conn_root = sqlite3.connect(db_root)
cursor_root = conn_root.cursor()

conn_inst = sqlite3.connect(db_instance_bak)
cursor_inst = conn_inst.cursor()

# 1. Migrate Root DB (Add payment_method to ledger)
try:
    print("Migrating ledger table...")
    cursor_root.execute("ALTER TABLE ledger ADD COLUMN payment_method VARCHAR(20) DEFAULT 'Cash'")
    print("Added payment_method column.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e).lower():
        print("payment_method column already exists.")
    else:
        print(f"Migration error: {e}")

# 2. Clear existing tenants/ledger in root to prevent conflicts (Fresh start for merge)
print("Clearing existing root data to ensure clean merge...")
cursor_root.execute("DELETE FROM ledger")
cursor_root.execute("DELETE FROM billing_profiles")
cursor_root.execute("DELETE FROM tenants")

# 3. Get all data from instance bak
cursor_inst.execute("SELECT * FROM tenants")
tenants = cursor_inst.fetchall()
cursor_inst.execute("PRAGMA table_info(tenants)")
tenant_cols = [col[1] for col in cursor_inst.fetchall()]

cursor_inst.execute("SELECT * FROM billing_profiles")
billing = cursor_inst.fetchall()
cursor_inst.execute("PRAGMA table_info(billing_profiles)")
billing_cols = [col[1] for col in cursor_inst.fetchall()]

cursor_inst.execute("SELECT * FROM ledger")
ledger = cursor_inst.fetchall()
cursor_inst.execute("PRAGMA table_info(ledger)")
ledger_cols = [col[1] for col in cursor_inst.fetchall()]

# 4. Insert data into root
def insert_table(cursor, table, cols, rows):
    if not rows: return
    placeholders = ",".join(["?"] * len(cols))
    sql = f"INSERT INTO {table} ({','.join(cols)}) VALUES ({placeholders})"
    cursor.executemany(sql, rows)

print(f"Merging {len(tenants)} tenants...")
insert_table(cursor_root, "tenants", tenant_cols, tenants)

print(f"Merging {len(billing)} billing profiles...")
insert_table(cursor_root, "billing_profiles", billing_cols, billing)

print(f"Merging {len(ledger)} ledger entries...")
insert_table(cursor_root, "ledger", ledger_cols, ledger)

conn_root.commit()
print("Data merge complete.")

conn_root.close()
conn_inst.close()
