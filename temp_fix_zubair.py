import sqlite3
import os

db_path = 'instance/hostel.db'
if not os.path.exists(db_path):
    print(f"Error: {db_path} not found")
    exit(1)

connection = sqlite3.connect(db_path, timeout=30)
cursor = connection.cursor()

try:
    # 1. Find Zubair's ID
    cursor.execute("SELECT id, name FROM tenants WHERE name LIKE 'Zubair%'")
    zubair = cursor.fetchone()
    
    if zubair:
        zid = zubair[0]
        zname = zubair[1]
        print(f"Found Zubair: ID={zid}, Name={zname}")
        
        # Check current ledger for DEPOSIT entries
        cursor.execute("SELECT amount, status, type FROM ledger WHERE tenant_id=? AND type='DEPOSIT' AND deleted_at IS NULL", (zid,))
        deposits = cursor.fetchall()
        print(f"Current Deposits for {zname}: {deposits}")
        
        # Total security should be 5000 according to user context
        # If there's only a 4000 PAID entry, add a 1000 PENDING one.
        total_paid = sum(float(d[0]) for d in deposits if d[1] == 'PAID')
        total_pending = sum(float(d[0]) for d in deposits if d[1] == 'PENDING')
        
        print(f"Accounting: Paid={total_paid}, Pending={total_pending}")

        if total_paid == 4000 and total_pending == 0:
            print("Action: Adding 1000 PENDING security deposit entry.")
            cursor.execute("""
                INSERT INTO ledger (tenant_id, amount, type, status, description, timestamp) 
                VALUES (?, 1000.00, 'DEPOSIT', 'PENDING', 'Security Deposit Arrears (Manual Fix)', datetime('now'))
            """, (zid,))
            connection.commit()
            print("Successfully added 1000 PENDING entry for Zubair.")
        else:
            print(f"No changes needed: Zubair has Total Paid={total_paid}, Total Pending={total_pending}")
    else:
        print("Zubair not found in database.")

except Exception as e:
    print(f"Error: {str(e)}")
finally:
    connection.close()
