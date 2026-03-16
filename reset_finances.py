from backend.app import create_app
from backend.models import db, Ledger, Expense, MeterReading, WaterBill, InternetBill

app = create_app()

def reset_finances():
    with app.app_context():
        try:
            print("Deleting all ledger entries...")
            Ledger.query.delete()
            
            print("Deleting all expense records...")
            Expense.query.delete()
            
            print("Deleting all utility readings/bills...")
            MeterReading.query.delete()
            WaterBill.query.delete()
            InternetBill.query.delete()
            
            db.session.commit()
            print("Financial data reset to zero successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error resetting financials: {e}")

if __name__ == "__main__":
    reset_finances()
