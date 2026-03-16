import sqlite3
import os

DB_PATH = 'hostel.db'

def check_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("--- Tenants Data ---")
    c.execute("SELECT id, name, id_card_front_url, id_card_back_url, police_form_url FROM tenants LIMIT 5")
    rows = c.fetchall()
    for r in rows:
        print(f"ID: {r[0]}, Name: {r[1]}")
        print(f"  Front: {r[2]}")
        print(f"  Back:  {r[3]}")
        print(f"  Form:  {r[4]}")
        
    print("\n--- Documents Table ---")
    c.execute("SELECT id, tenant_id, type, url FROM documents ORDER BY id DESC LIMIT 10")
    docs = c.fetchall()
    for d in docs:
        print(f"ID: {d[0]}, Tenant: {d[1]}, Type: {d[2]}, URL: {d[3]}")
        
    conn.close()

if __name__ == "__main__":
    check_data()
