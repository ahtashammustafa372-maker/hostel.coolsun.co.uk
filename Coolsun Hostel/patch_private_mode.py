from backend.app import create_app
from backend.models import db
from sqlalchemy import text

app = create_app()

def patch_db():
    with app.app_context():
        try:
            print("Adding tenancy_type column to tenants...")
            # SQLite handles Enum as VARCHAR by default in SQLAlchemy
            db.session.execute(text("ALTER TABLE tenants ADD COLUMN tenancy_type VARCHAR(20) DEFAULT 'Shared'"))
            db.session.commit()
            print("Database patched successfully!")
        except Exception as e:
            print(f"Error patching database: {e}")
            db.session.rollback()

if __name__ == "__main__":
    patch_db()
