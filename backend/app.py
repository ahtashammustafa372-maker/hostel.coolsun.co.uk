from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from backend.models import db
import os

# ─── Absolute DB path ────────────────────────────────────────────────────────
# Always resolve relative to THIS file's directory (backend/), so the DB path
# never changes regardless of which directory Flask is launched from.
_BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_DB_PATH = os.path.join(_BASE_DIR, 'hostel.db')

def create_app():
    # Configure Flask to serve static files from the React dist folder securely
    _FRONTEND_DIST = os.path.abspath(os.path.join(_BASE_DIR, 'frontend', 'dist'))
    app = Flask(__name__, static_folder=_FRONTEND_DIST, static_url_path='/')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{_DB_PATH}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev_key'
    
    # ─── Production Security ─────────────────────────────────────────────────────
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    
    # ─── Cloudflare Proxy Fix ───────────────────────────────────────────────────
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # ─── CORS ───────────────────────────────────────────────────────────────────
    CORS(app, resources={r"/api/*": {"origins": "https://hostel.coolsun.co.uk"}})

    db.init_app(app)

    # Auto-create tables on first run (safe to call repeatedly)
    with app.app_context():
        db.create_all()

    # Register Blueprints
    from backend.routes.onboarding import onboarding_bp
    from backend.routes.dashboard import dashboard_bp
    from backend.routes.rooms import rooms_bp
    from backend.routes.tenants import tenants_bp
    from backend.routes.utilities import utilities_bp
    from backend.routes.police import police_bp
    from backend.routes.settings import settings_bp
    from backend.routes.tasks import tasks_bp
    from backend.routes.moveout import moveout_bp
    from backend.routes.finance import finance_bp

    app.register_blueprint(onboarding_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp, url_prefix='/api')
    app.register_blueprint(rooms_bp, url_prefix='/api')
    app.register_blueprint(tenants_bp, url_prefix='/api')
    app.register_blueprint(utilities_bp, url_prefix='/api')
    app.register_blueprint(police_bp, url_prefix='/api')
    app.register_blueprint(settings_bp, url_prefix='/api')
    app.register_blueprint(tasks_bp, url_prefix='/api')
    app.register_blueprint(moveout_bp, url_prefix='/api')
    app.register_blueprint(finance_bp, url_prefix='/api')

    @app.route('/api/debug/patch-db')
    def patch_db():
        from sqlalchemy import text
        try:
            db.session.execute(text("ALTER TABLE rooms ADD COLUMN base_rent DECIMAL(10,2) DEFAULT 10000.00"))
            db.session.commit()
            return "Database patched successfully!", 200
        except Exception as e:
            if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                return "Column already exists", 200
            return f"Error: {str(e)}", 500

    @app.route('/api/debug/db-info')
    def db_info():
        import os
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        # Extract path from sqlite:///path
        db_path = db_uri.replace('sqlite:///', '')
        abs_path = os.path.abspath(db_path)
        exists = os.path.exists(abs_path)
        return jsonify({
            "db_uri": db_uri,
            "abs_path": abs_path,
            "exists": exists,
            "cwd": os.getcwd()
        }), 200

    @app.route('/api/debug/fix201')
    def fix201():
        from backend.models import Ledger, Tenant, Room
        from datetime import datetime
        
        # 1. Target Room 201
        room = Room.query.filter_by(number='201').first()
        if not room: return "Room 201 not found", 404
        
        # 2. Get specific tenants in that room
        tenants = Tenant.query.filter_by(room_id=room.id).all()
        # Filter for Ahtasham and Zubair specifically
        ahtasham = next((t for t in tenants if 'Ahtasham' in t.name), None)
        zubair = next((t for t in tenants if 'Zubair' in t.name), None)
        
        if not ahtasham or not zubair:
            return f"Tenants not found: Aht={ahtasham}, Zub={zubair}", 404
            
        # 3. Wipe their ledger
        Ledger.query.filter(Ledger.tenant_id.in_([ahtasham.id, zubair.id])).delete(synchronize_session=False)
        
        # 4. Create Ahtasham entries (5k Sec, 5k Rent - BOTH PAID)
        db.session.add(Ledger(tenant_id=ahtasham.id, amount=5000, type='DEPOSIT', status='PAID', description='Manual Correction: Security Deposit'))
        db.session.add(Ledger(tenant_id=ahtasham.id, amount=5000, type='RENT', status='PAID', description='Manual Correction: Rent'))
        
        # 5. Create Zubair entries (5k Sec PAID, 4k Rent PAID, 1k Rent PENDING)
        db.session.add(Ledger(tenant_id=zubair.id, amount=5000, type='DEPOSIT', status='PAID', description='Manual Correction: Security Deposit'))
        db.session.add(Ledger(tenant_id=zubair.id, amount=4000, type='RENT', status='PAID', description='Manual Correction: Rent Paid'))
        db.session.add(Ledger(tenant_id=zubair.id, amount=1000, type='RENT', status='PENDING', description='Manual Correction: Rent Balance'))
        
        db.session.commit()
        return f"Room 201 (IDs: {ahtasham.id}, {zubair.id}) reset success.", 200

    @app.route('/api/debug/ping')
    def ping():
        return "pong", 200

    # ─── SPA Fallback Route ─────────────────────────────────────────────────────
    # Serve React App for any route that doesn't start with /api
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        # If the path is a file that exists in the dist folder, serve it
        full_path = os.path.join(app.static_folder, path)
        if path != "" and os.path.exists(full_path):
            return send_from_directory(app.static_folder, path)
        # Otherwise, let React Router handle the route client-side via index.html
        return send_from_directory(app.static_folder, 'index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
