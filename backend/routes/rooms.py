from flask import Blueprint, request, jsonify
from backend.models import db, Room, Tenant
from sqlalchemy.exc import IntegrityError

rooms_bp = Blueprint('rooms', __name__)

@rooms_bp.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.filter_by(deleted_at=None).all()
    result = []
    for room in rooms:
        active_tenants = room.get_active_tenants()
        result.append({
            "id": room.id,
            "number": room.number,
            "floor": room.floor,
            "type": room.type,
            "capacity": room.capacity,
            "base_rent": float(room.base_rent or 0),
            "occupied_beds": len(active_tenants),
            "available_slots": room.available_slots
        })
    return jsonify(result), 200

@rooms_bp.route('/rooms/<int:room_id>', methods=['PUT'])
def update_room(room_id):
    room = Room.query.get_or_404(room_id)
    data = request.json
    
    # Logic Guard: Capacity cannot be less than active tenants
    active_tenants_count = len(room.get_active_tenants())
    new_capacity = data.get('capacity', room.capacity)
    
    if new_capacity < active_tenants_count:
        return jsonify({
            "error": "Conflict", 
            "message": f"Cannot reduce capacity to {new_capacity}. Room has {active_tenants_count} active tenants."
        }), 409

    try:
        room.number = data.get('number', room.number)
        room.type = data.get('type', room.type)
        room.capacity = new_capacity
        room.base_rent = float(data.get('base_rent', room.base_rent))
        room.floor = int(data.get('floor', room.floor))
        
        db.session.commit()
        return jsonify({"message": "Room updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@rooms_bp.route('/rooms', methods=['POST'])
def create_room():
    data = request.json
    
    # 0. Strict Validation for required fields
    required_fields = ['number', 'floor', 'type', 'capacity', 'base_rent']
    for field in required_fields:
        if field not in data or data[field] == '' or data[field] is None:
            return jsonify({
                "error": "Missing Field",
                "message": f"The '{field}' field is required and cannot be empty."
            }), 400
            
    number = str(data.get('number', '')).strip()
    
    # 1. Check for Duplicate Room Number
    existing = Room.query.filter_by(number=number, deleted_at=None).first()
    if existing:
        return jsonify({
            "error": "Duplicate Room",
            "message": f"Room '{number}' already exists in the inventory."
        }), 409

    try:
        new_room = Room(
            floor=int(data.get('floor', 1)),
            number=number,
            type=data.get('type', 'Small'),
            capacity=int(data.get('capacity', 2)),
            base_rent=float(data.get('base_rent', 10000.00))
        )
        db.session.add(new_room)
        db.session.commit()
        return jsonify({"message": "Room created successfully", "id": new_room.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@rooms_bp.route('/rooms/<int:room_id>', methods=['DELETE'])
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    if len(room.get_active_tenants()) > 0:
        return jsonify({"error": "Cannot delete room with active tenants"}), 409
    try:
        room.delete()
        db.session.commit()
        return jsonify({"message": "Room deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

