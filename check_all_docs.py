import sqlite3

def check_all_docs():
    conn = sqlite3.connect('hostel.db')
    c = conn.cursor()
    
    print("--- All Documents for Tenant 2 (Ahad) ---")
    c.execute("SELECT id, type, url FROM documents WHERE tenant_id = 2")
    for r in c.fetchall():
        print(f"ID: {r[0]}, Type: {r[1]}, URL: {r[2]}")
        
    print("\n--- All Documents for Tenant 1 (Ahtasham) ---")
    c.execute("SELECT id, type, url FROM documents WHERE tenant_id = 1")
    for r in c.fetchall():
        print(f"ID: {r[0]}, Type: {r[1]}, URL: {r[2]}")

    print("\n--- Any document with 'back' in type or URL ---")
    c.execute("SELECT id, tenant_id, type, url FROM documents WHERE type LIKE '%back%' OR url LIKE '%back%'")
    for r in c.fetchall():
        print(f"ID: {r[0]}, Tenant: {r[1]}, Type: {r[2]}, URL: {r[3]}")

    conn.close()

if __name__ == "__main__":
    check_all_docs()
