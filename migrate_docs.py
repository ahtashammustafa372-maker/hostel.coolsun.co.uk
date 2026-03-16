import os
import shutil
import sqlite3

# Target directory for all documents
TARGET_DIR = os.path.join('backend', 'static', 'uploads', 'documents')
WEB_PATH_BASE = '/static/uploads/documents/'
DB_PATH = 'hostel.db'

def migrate():
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        print(f"Created directory: {TARGET_DIR}")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. Map lower-case or inconsistent types to official Enum values
    type_mapping = {
        'id_front': 'ID_Front',
        'id_back': 'ID_Back',
        'agreement': 'Agreement',
        'police_form': 'Police_Form'
    }

    print("--- Normalizing Document Table types ---")
    for old, new in type_mapping.items():
        c.execute("UPDATE documents SET type = ? WHERE type = ?", (new, old))
    conn.commit()

    print("--- Consolidating files and updating URLs ---")
    
    # Process Document table
    rows = c.execute("SELECT id, url FROM documents").fetchall()
    for doc_id, old_url in rows:
        filename = os.path.basename(old_url.replace('\\', '/'))
        
        # Source path candidates
        sources = [
            os.path.join('backend', 'uploads', filename),
            os.path.join('backend', 'static', 'uploads', 'police_forms', filename),
            os.path.join('uploads', filename)
        ]
        
        moved = False
        for src in sources:
            if os.path.exists(src):
                dest = os.path.join(TARGET_DIR, filename)
                if not os.path.exists(dest) or os.path.abspath(src) != os.path.abspath(dest):
                    shutil.copy2(src, dest)
                    print(f"  Copied {src} -> {dest}")
                
                new_url = f"{WEB_PATH_BASE}{filename}"
                c.execute("UPDATE documents SET url = ? WHERE id = ?", (new_url, doc_id))
                moved = True
                break
        
        if not moved:
            print(f"  WARNING: Source file for {filename} not found!")
            if 'static' not in old_url:
                new_url = f"{WEB_PATH_BASE}{filename}"
                c.execute("UPDATE documents SET url = ? WHERE id = ?", (new_url, doc_id))

    # Process Tenant table
    tenant_rows = c.execute("SELECT id, id_card_front_url, id_card_back_url, police_form_url FROM tenants").fetchall()
    for t_id, front, back, form in tenant_rows:
        updates = []
        params = []
        if front and 'static' not in front:
            filename = os.path.basename(front.replace('\\', '/'))
            updates.append("id_card_front_url = ?")
            params.append(f"{WEB_PATH_BASE}{filename}")
        if back and 'static' not in back:
            filename = os.path.basename(back.replace('\\', '/'))
            updates.append("id_card_back_url = ?")
            params.append(f"{WEB_PATH_BASE}{filename}")
        if form and '/static/uploads/documents/' not in form:
             # Form might already be in /static/uploads/police_forms, move it
            filename = os.path.basename(form.replace('\\', '/'))
            # Check source if it's in the old location
            old_loc = os.path.join('backend', 'static', 'uploads', 'police_forms', filename)
            if os.path.exists(old_loc):
                dest = os.path.join(TARGET_DIR, filename)
                shutil.copy2(old_loc, dest)
                print(f"  Copied {old_loc} -> {dest} (tenant field sync)")
            
            updates.append("police_form_url = ?")
            params.append(f"{WEB_PATH_BASE}{filename}")
        
        if updates:
            sql = f"UPDATE tenants SET {', '.join(updates)} WHERE id = ?"
            params.append(t_id)
            c.execute(sql, params)

    conn.commit()
    conn.close()
    print("\nMigration complete. Raw SQL updates finished.")

if __name__ == "__main__":
    migrate()
