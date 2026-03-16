from backend.app import create_app
from backend.models import db, Tenant
from sqlalchemy import inspect

app = create_app()
with app.app_context():
    inst = inspect(Tenant)
    print("Columns in 'tenants' table:")
    for c in inst.mapper.column_attrs:
        print(f"- {c.key}")
