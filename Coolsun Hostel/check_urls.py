from backend.app import create_app
from backend.models import db, Tenant, Document

app = create_app()

def check_urls():
    with app.app_context():
        print("--- Tenant URLs ---")
        tenants = Tenant.query.all()
        for t in tenants:
            print(f"ID: {t.id}, Name: {t.name}")
            print(f"  Front: {t.id_card_front_url}")
            print(f"  Back:  {t.id_card_back_url}")
            print(f"  Form:  {t.police_form_url}")
        
        print("\n--- Document Table URLs ---")
        docs = Document.query.all()
        for d in docs:
            print(f"ID: {d.id}, TenantID: {d.tenant_id}, Type: {d.type}, URL: {d.url}")

if __name__ == "__main__":
    check_urls()
