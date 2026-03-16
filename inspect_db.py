from backend.app import create_app
from backend.models import db
from sqlalchemy import inspect

app = create_app()

def inspect_db():
    with app.app_context():
        inspector = inspect(db.engine)
        columns = inspector.get_columns('billing_profiles')
        print("Columns in billing_profiles:")
        for column in columns:
            print(f"- {column['name']} ({column['type']})")

if __name__ == "__main__":
    inspect_db()
