import sqlite3

DB_PATH = 'hostel.db'

def sync_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("--- Syncing Tenants with Documents ---")
    
    # 1. Get all active documents
    c.execute("SELECT tenant_id, type, url FROM documents WHERE deleted_at IS NULL")
    docs = c.fetchall()
    
    # Map types to tenant table columns
    column_mapping = {
        'ID_Front': 'id_card_front_url',
        'ID_Back': 'id_card_back_url',
        'Police_Form': 'police_form_url'
    }
    
    updates = 0
    for tenant_id, doc_type, url in docs:
        if doc_type in column_mapping:
            column = column_mapping[doc_type]
            print(f"  Syncing Tenant {tenant_id}: {doc_type} -> {url}")
            c.execute(f"UPDATE tenants SET {column} = ? WHERE id = ?", (url, tenant_id))
            updates += 1
            
    conn.commit()
    conn.close()
    print(f"\nSync complete. {updates} fields updated.")

if __name__ == "__main__":
    sync_data()
