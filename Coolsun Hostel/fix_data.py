import sqlite3
import os
from datetime import datetime

db_path = r'd:\Coolsun Hostel\Coolsun Hostel\backend\instance\hostel.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Delete Test Tenants and their Ledger entries
cursor.execute("SELECT id FROM tenants WHERE name LIKE 'Test%'")
test_tenant_ids = [row[0] for row in cursor.fetchall()]
for tid in test_tenant_ids:
    cursor.execute("DELETE FROM ledger WHERE tenant_id = ?", (tid,))
    cursor.execute("DELETE FROM tenants WHERE id = ?", (tid,))

# 2. Update Ahtasham Mustafa (ID 4)
# Current: 13,500 Rent, 15,000 Security
# Target: 13,500 Rent, 5,000 Security
cursor.execute("UPDATE ledger SET amount = 5000 WHERE tenant_id = 4 AND type = 'DEPOSIT'")

# 3. Create Junaid
# Target: 9,500 Rent, 5,000 Security
# Need a Room ID. Ahtasham is in Room ID 2? Let's check.
cursor.execute("SELECT room_id FROM tenants WHERE id = 4")
room_id = cursor.fetchone()[0]

cursor.execute("""
    INSERT INTO tenants (name, cnic, phone, room_id, police_status, agreement_start_date, actual_move_in_date, bed_label)
    VALUES ('Junaid', '12345-1234567-1', '0300-1234567', ?, 'Verified', '2026-03-01', '2026-03-01', 'Lower Berth')
""", (room_id,))
junaid_id = cursor.lastrowid

# Junaid's Security (5,000)
cursor.execute("""
    INSERT INTO ledger (tenant_id, amount, type, status, timestamp, description, payment_method)
    VALUES (?, 5000, 'DEPOSIT', 'PAID', ?, 'Initial Security Deposit', 'Cash')
""", (junaid_id, datetime.utcnow()))

# Junaid's Rent (9,500)
cursor.execute("""
    INSERT INTO ledger (tenant_id, amount, type, status, timestamp, description, payment_method)
    VALUES (?, 9500, 'RENT', 'PAID', ?, 'Initial Rent (Paid)', 'Cash')
""", (junaid_id, datetime.utcnow()))

conn.commit()
conn.close()
print("Data fix completed.")
