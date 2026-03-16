from backend.app import create_app
from backend.models import db, Tenant

app = create_app()
with app.app_context():
    tenant = Tenant.query_active().first()
    if tenant:
        print(f"Active Tenant Found: {tenant.name} (ID: {tenant.id})")
    else:
        print("No active tenants found")
