from backend.app import create_app
from backend.models import db
from sqlalchemy import text

app = create_app()

def patch_db():
    with app.app_context():
        try:
            print("Adding security_deposit column to billing_profiles...")
            db.session.execute(text("ALTER TABLE billing_profiles ADD COLUMN security_deposit DECIMAL(10,2) DEFAULT 0"))
        except Exception as e:
            print(f"Error adding security_deposit: {e}")
            
        try:
            print("Adding pro_rata_rent column to billing_profiles...")
            db.session.execute(text("ALTER TABLE billing_profiles ADD COLUMN pro_rata_rent DECIMAL(10,2) DEFAULT 0"))
        except Exception as e:
            print(f"Error adding pro_rata_rent: {e}")
            
        db.session.commit()
        print("Database patched successfully!")

if __name__ == "__main__":
    patch_db()
