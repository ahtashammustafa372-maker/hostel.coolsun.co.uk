from backend.app import create_app
from backend.models import db
from sqlalchemy import text

app = create_app()

def patch_billing():
    with app.app_context():
        try:
            print("Adding security_deposit and pro_rata_rent to billing_profiles...")
            db.session.execute(text("ALTER TABLE billing_profiles ADD COLUMN security_deposit NUMERIC(10, 2) DEFAULT 0"))
            db.session.execute(text("ALTER TABLE billing_profiles ADD COLUMN pro_rata_rent NUMERIC(10, 2) DEFAULT 0"))
            db.session.commit()
            print("Database patched successfully!")
        except Exception as e:
            print(f"Error patching database: {e}")
            db.session.rollback()

if __name__ == "__main__":
    patch_billing()
