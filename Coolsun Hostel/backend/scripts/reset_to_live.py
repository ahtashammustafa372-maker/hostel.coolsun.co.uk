from backend.app import create_app
from backend.models import db, Tenant, BillingProfile, Expense, Document, Ledger, MaintenanceRequest, Task

app = create_app()

def nuclear_reset():
    with app.app_context():
        confirm = input("⚠️ WARNING: This will DELETE ALL Tenants, Expenses, and Billing Data. Only Rooms and Admin settings will remain. Type 'CONFIRM' to proceed: ")
        
        if confirm == 'CONFIRM':
            # Delete in order of dependency
            print("Cleaning Documents...")
            Document.query.delete()
            print("Cleaning Billing Profiles...")
            BillingProfile.query.delete()
            print("Cleaning Ledger...")
            Ledger.query.delete()
            print("Cleaning Maintenance Requests...")
            MaintenanceRequest.query.delete()
            print("Cleaning Tasks...")
            Task.query.delete()
            print("Cleaning Expenses...")
            Expense.query.delete()
            print("Cleaning Tenants...")
            Tenant.query.delete()
            
            db.session.commit()
            print("✅ NUCLEAR RESET COMPLETE. System is clean for Jan 1, 2026.")
        else:
            print("❌ Reset Cancelled.")

if __name__ == '__main__':
    nuclear_reset()
