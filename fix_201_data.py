from backend.app import create_app
from backend.models import db, Ledger, Tenant, Room
import sys

def fix():
    app = create_app()
    # Override DB path to instance/hostel.db which seems to be the active one
    import os
    db_abs_path = os.path.abspath('instance/hostel.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_abs_path}'
    
    with app.app_context():
        print(f"DEBUG: Using DB URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # 1. Target tenants globally
        ahtasham = Tenant.query.filter(Tenant.name.like('Ahtasham%')).first()
        zubair = Tenant.query.filter(Tenant.name.like('Zubair%')).first()
        
        if not ahtasham or not zubair:
            print(f"Tenants not found by name: Aht={ahtasham}, Zub={zubair}")
            return
            
        print(f"Cleaning up (Ahtasham ID: {ahtasham.id} '{ahtasham.name}', Zubair ID: {zubair.id} '{zubair.name}')...")
        
        if not ahtasham or not zubair:
            print(f"Tenants not found: Aht={ahtasham}, Zub={zubair}")
            return
            
        print(f"Cleaning up Room 201 (Ahtasham ID: {ahtasham.id}, Zubair ID: {zubair.id})...")
        
        # 3. Wipe their ledger (HARD DELETE for cleanup)
        Ledger.query.filter(Ledger.tenant_id.in_([ahtasham.id, zubair.id])).delete(synchronize_session=False)
        
        # 4. Create Ahtasham entries (5k Sec, 5k Rent - BOTH PAID)
        db.session.add(Ledger(tenant_id=ahtasham.id, amount=5000, type='DEPOSIT', status='PAID', description='Manual Correction: Security Deposit'))
        db.session.add(Ledger(tenant_id=ahtasham.id, amount=5000, type='RENT', status='PAID', description='Manual Correction: Rent'))
        
        # 5. Create Zubair entries (5k Sec PAID, 4k Rent PAID, 1k Rent PENDING)
        db.session.add(Ledger(tenant_id=zubair.id, amount=5000, type='DEPOSIT', status='PAID', description='Manual Correction: Security Deposit'))
        db.session.add(Ledger(tenant_id=zubair.id, amount=4000, type='RENT', status='PAID', description='Manual Correction: Rent Paid'))
        db.session.add(Ledger(tenant_id=zubair.id, amount=1000, type='RENT', status='PENDING', description='Manual Correction: Rent Balance'))
        
        db.session.commit()
        print("Success: Room 201 ledgers reset.")

if __name__ == "__main__":
    fix()
