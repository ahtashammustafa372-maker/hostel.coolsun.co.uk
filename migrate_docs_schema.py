import sqlite3
import os

db_path = 'hostel.db'

def migrate():
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        columns = [
            ('id_card_front_url', 'TEXT'),
            ('id_card_back_url', 'TEXT'),
            ('police_form_url', 'TEXT')
        ]
        
        for col_name, col_type in columns:
            try:
                print(f"Adding column {col_name} to tenants table...")
                cursor.execute(f"ALTER TABLE tenants ADD COLUMN {col_name} {col_type}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e).lower():
                    print(f"Column {col_name} already exists.")
                else:
                    raise e
        
        conn.commit()
        print("Migration completed successfully.")
        conn.close()
    except Exception as e:
        print(f"An error occurred during migration: {e}")

if __name__ == "__main__":
    migrate()
