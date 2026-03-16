from backend.app import create_app
from backend.models import db, Tenant

app = create_app()
with app.app_context():
    # Try to delete the test tenant we just created (Room 102 Test)
    tenant = Tenant.query.filter_by(name="Room 102 Test").first()
    if tenant:
        print(f"Deleting tenant: {tenant.name} (ID: {tenant.id})")
        tenant.delete()
        db.session.commit()
        print("Success")
    else:
        print("Tenant 'Room 102 Test' not found")
