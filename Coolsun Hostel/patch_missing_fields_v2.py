import sqlite3
import os

DB_PATHS = [
    r'D:\Coolsun Hostel\Coolsun Hostel\instance\hostel.db',
    r'D:\Coolsun Hostel\Coolsun Hostel\backend\instance\hostel.db',
    r'D:\Coolsun Hostel\Coolsun Hostel\backend\hostel.db',
    r'D:\Coolsun Hostel\Coolsun Hostel\hostel.db',
]

def patch_db(db_path):
    if not os.path.exists(db_path):
        return
    print(f"Patching {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    def try_add(sql, label):
        try:
            cursor.execute(sql)
            print(f"  [OK] Added {label}")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower() or "already exists" in str(e).lower() or "duplicate" in str(e).lower() or "already" in str(e).lower():
                print(f"  [SKIP] {label} already exists.")
            else:
                print(f"  [ERROR] {label}: {e}")

    # Patch Rooms
    try_add("ALTER TABLE rooms ADD COLUMN base_rent DECIMAL(10,2) DEFAULT 10000.00", "rooms.base_rent")

    # Patch Tenants
    tenant_cols = [
        ("police_status", "VARCHAR(20) DEFAULT 'Pending'"),
        ("police_form_submitted", "DATETIME"),
        ("father_name", "VARCHAR(100)"),
        ("permanent_address", "TEXT"),
        ("police_station", "VARCHAR(100)"),
        ("compliance_alert", "BOOLEAN DEFAULT False"),
        ("agreement_start_date", "DATE"),
        ("actual_move_in_date", "DATE"),
        ("bed_label", "VARCHAR(50)"),
        ("cnic_expiry_date", "DATE"),
        ("is_partial_payment", "BOOLEAN DEFAULT False"),
        ("internet_opt_in", "BOOLEAN DEFAULT True"),
        ("parent_tenant_id", "INTEGER"),
        ("deleted_at", "DATETIME")
    ]

    for col_name, col_type in tenant_cols:
        try_add(f"ALTER TABLE tenants ADD COLUMN {col_name} {col_type}", f"tenants.{col_name}")

    conn.commit()
    conn.close()
    print("Done.\n")

if __name__ == '__main__':
    for p in DB_PATHS:
        patch_db(p)
