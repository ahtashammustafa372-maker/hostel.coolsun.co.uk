import sqlite3

def upgrade_db():
    conn = sqlite3.connect(r'D:\Coolsun Hostel\Coolsun Hostel\backend\instance\hostel.db')
    cursor = conn.cursor()
    
    try:
        # Add parent_tenant_id column to tenants table
        cursor.execute("ALTER TABLE tenants ADD COLUMN parent_tenant_id INTEGER REFERENCES tenants(id)")
        print("Successfully added parent_tenant_id to tenants table")
    except sqlite3.OperationalError as e:
        print(f"Column might already exist or error occurred: {e}")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    upgrade_db()
