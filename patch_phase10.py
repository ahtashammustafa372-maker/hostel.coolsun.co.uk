"""
patch_phase10.py - Adds new tables and columns for Phase 10-12 features.
Run once: python patch_phase10.py
"""
import sqlite3

DB_PATH = r'D:\Coolsun Hostel\Coolsun Hostel\backend\instance\hostel.db'
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

def try_add(sql, label):
    try:
        cursor.execute(sql)
        print(f"✅ {label}")
    except sqlite3.OperationalError as e:
        print(f"⚠️  Skipped {label}: {e}")

# 1. New columns on expenses
try_add("ALTER TABLE expenses ADD COLUMN receipt_url VARCHAR(255)", "expenses.receipt_url")
try_add("ALTER TABLE expenses ADD COLUMN approval_status VARCHAR(20) DEFAULT 'Pending'", "expenses.approval_status")
try_add("ALTER TABLE expenses ADD COLUMN submitted_by INTEGER", "expenses.submitted_by")
try_add("ALTER TABLE expenses ADD COLUMN approved_by INTEGER", "expenses.approved_by")
try_add("ALTER TABLE expenses ADD COLUMN approved_at DATETIME", "expenses.approved_at")

# 2. Fine Types table
cursor.execute("""
CREATE TABLE IF NOT EXISTS fine_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    amount NUMERIC(10,2) NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME
)
""")
print("✅ fine_types table")

# 3. Audit Logs table (immutable — no deleted_at)
cursor.execute("""
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action VARCHAR(200) NOT NULL,
    entity VARCHAR(100),
    entity_id INTEGER,
    details TEXT,
    ip_address VARCHAR(45),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
print("✅ audit_logs table")

# 4. Staff Members table
cursor.execute("""
CREATE TABLE IF NOT EXISTS staff_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL,
    phone VARCHAR(20),
    salary NUMERIC(10,2),
    joined_at DATE,
    deleted_at DATETIME
)
""")
print("✅ staff_members table")

# 5. Staff Attendance table
cursor.execute("""
CREATE TABLE IF NOT EXISTS staff_attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff_id INTEGER NOT NULL,
    date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Present',
    time_in VARCHAR(10),
    time_out VARCHAR(10),
    notes TEXT,
    FOREIGN KEY (staff_id) REFERENCES staff_members(id)
)
""")
print("✅ staff_attendance table")

# 6. Move-Out Records table
cursor.execute("""
CREATE TABLE IF NOT EXISTS move_out_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id INTEGER NOT NULL,
    notice_date DATE NOT NULL,
    exit_date DATE NOT NULL,
    security_deposit_held NUMERIC(10,2) DEFAULT 0,
    damage_deduction NUMERIC(10,2) DEFAULT 0,
    fine_deduction NUMERIC(10,2) DEFAULT 0,
    unpaid_rent NUMERIC(10,2) DEFAULT 0,
    refund_amount NUMERIC(10,2) DEFAULT 0,
    notes TEXT,
    approved_by INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
)
""")
print("✅ move_out_records table")

# 7. Seed default fine types if empty
cursor.execute("SELECT COUNT(*) FROM fine_types")
if cursor.fetchone()[0] == 0:
    defaults = [
        ('Late Rent Fine', 500, 'Applied after 5th of month grace period'),
        ('Property Damage', 1000, 'Deducted if tenant damages room or facility'),
        ('Smoking Violation', 2000, 'Hostel is non-smoking'),
        ('Early Exit (No Notice)', 5000, 'Penalty for leaving without 30-day notice'),
    ]
    cursor.executemany("INSERT INTO fine_types (name, amount, description) VALUES (?, ?, ?)", defaults)
    print("✅ Seeded 4 default fine types")

conn.commit()
conn.close()
print("\n🎉 Phase 10-12 database patch complete.")
