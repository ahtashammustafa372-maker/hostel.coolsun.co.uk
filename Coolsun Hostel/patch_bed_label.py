"""
patch_bed_label.py - Adds bed_label, cnic_expiry_date, is_partial_payment columns
to the tenants table in all hostel.db files.
Run once: python patch_bed_label.py
"""
import sqlite3
import os

DB_PATHS = [
    r'D:\Coolsun Hostel\Coolsun Hostel\instance\hostel.db',
    r'D:\Coolsun Hostel\Coolsun Hostel\backend\instance\hostel.db',
    r'D:\Coolsun Hostel\Coolsun Hostel\backend\hostel.db',
]

def patch_db(path):
    if not os.path.exists(path):
        print(f"⏭️  Skipping (not found): {path}")
        return
    print(f"\n📂 Patching: {path}")
    conn = sqlite3.connect(path)
    c = conn.cursor()

    def try_add(sql, label):
        try:
            c.execute(sql)
            print(f"  ✅ {label}")
        except sqlite3.OperationalError as e:
            print(f"  ⚠️  Skipped {label}: {e}")

    try_add("ALTER TABLE tenants ADD COLUMN bed_label VARCHAR(50)", "tenants.bed_label")
    try_add("ALTER TABLE tenants ADD COLUMN cnic_expiry_date DATE", "tenants.cnic_expiry_date")
    try_add("ALTER TABLE tenants ADD COLUMN is_partial_payment BOOLEAN DEFAULT 0", "tenants.is_partial_payment")

    conn.commit()
    conn.close()
    print(f"  🎉 Done")

for p in DB_PATHS:
    patch_db(p)

print("\n✅ bed_label patch complete on all DBs.")
