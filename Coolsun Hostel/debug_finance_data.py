from backend.app import create_app
from backend.models import db, Tenant, Ledger, Room

app = create_app()
with app.app_context():
    print("--- Tenants ---")
    tenants = Tenant.query.all()
    for t in tenants:
        print(f"ID: {t.id}, Name: {t.name}, Room: {t.room.number if t.room else 'N/A'}, Deleted: {t.deleted_at}")
    
    print("\n--- Ledger Entries ---")
    ledgers = Ledger.query.all()
    for l in ledgers:
        print(f"ID: {l.id}, TenantID: {l.tenant_id}, Type: {l.type}, Amount: {l.amount}, Status: {l.status}, Deleted: {l.deleted_at}")

    print("\n--- Summary Check ---")
    from sqlalchemy import func
    collected = db.session.query(func.sum(Ledger.amount)).filter(
        Ledger.type.in_(['RENT', 'PRIVATE_RENT', 'DEPOSIT']),
        Ledger.status == 'PAID',
        Ledger.deleted_at == None
    ).scalar() or 0.0
    print(f"Total Collected (Calculated): {collected}")
