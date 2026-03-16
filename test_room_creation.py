from backend.app import create_app
from backend.models import db, Room
import os

app = create_app()
with app.app_context():
    print(f"Current DB URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Try to create room 101 again
    try:
        new_room = Room(
            floor=1,
            number="101",
            type="Medium",
            capacity=3,
            base_rent=15000.00
        )
        db.session.add(new_room)
        db.session.commit()
        print("Success! Room 101 created (duplicate number).")
    except Exception as e:
        db.session.rollback()
        print(f"Caught Error: {type(e).__name__}: {str(e)}")

    # Try to create a new unique room
    try:
        new_room = Room(
            floor=1,
            number="999",
            type="Small",
            capacity=2,
            base_rent=8000.00
        )
        db.session.add(new_room)
        db.session.commit()
        print("Success! Room 999 created.")
        # Clean up
        db.session.delete(new_room)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error creating unique room: {type(e).__name__}: {str(e)}")
