import sqlite3
import os

db_path = 'hostel.db'

if not os.path.exists(db_path):
    print(f"Error: Database file not found at {db_path}")
    exit(1)

tables_to_clear = [
    'ledger',
    'expenses',
    'meter_readings',
    'water_bills',
    'internet_bills',
    'maintenance_requests',
    'tasks',
    'documents',
    'move_out_records',
    'tenants',
    'billing_profiles',
    'staff_members',
    'staff_attendance',
    'audit_logs',
    'fine_types'
]

def reset_database():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Disable foreign key constraints temporarily to avoid deletion order issues
        cursor.execute("PRAGMA foreign_keys = OFF;")
        
        for table in tables_to_clear:
            print(f"Clearing table: {table}")
            cursor.execute(f"DELETE FROM {table};")
            # Reset autoincrement sequences if they exist
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}';")
            
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        conn.commit()
        print("\nDatabase reset successful. All transaction and tenant data cleared.")
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    reset_database()
