"""
backend/routes/tasks.py
Micro-Tasking System + Staff Attendance
"""
from flask import Blueprint, request, jsonify
from backend.models import db, Task, StaffMember, StaffAttendance, MaintenanceRequest
from datetime import datetime, date

tasks_bp = Blueprint('tasks', __name__)


# ─────── TASK CRUD ───────
...
@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.delete()
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200


# ─────── MAINTENANCE REQUESTS ───────

@tasks_bp.route('/maintenance', methods=['GET'])
def get_maintenance():
    status_filter = request.args.get('status')
    q = MaintenanceRequest.query.filter_by(deleted_at=None)
    if status_filter:
        q = q.filter_by(status=status_filter)
    
    requests = q.order_by(MaintenanceRequest.created_at.desc()).all()
    return jsonify([{
        "id": r.id,
        "description": r.description,
        "priority": r.priority,
        "status": r.status,
        "is_approved": r.is_approved,
        "assigned_to": r.assigned_to,
        "created_at": r.created_at.isoformat() if r.created_at else None,
        "tenant_id": r.tenant_id
    } for r in requests]), 200


@tasks_bp.route('/maintenance', methods=['POST'])
def create_maintenance():
    data = request.json
    if not data.get('description'):
        return jsonify({"error": "Description required"}), 400
    
    try:
        req = MaintenanceRequest(
            description=data['description'],
            priority=data.get('priority', 'Routine'),
            status='Pending',
            tenant_id=data.get('tenant_id'),
            assigned_to=data.get('assigned_to')
        )
        db.session.add(req)
        db.session.commit()
        return jsonify({"message": "Maintenance request created", "id": req.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@tasks_bp.route('/maintenance/<int:req_id>', methods=['PUT'])
def update_maintenance(req_id):
    req = MaintenanceRequest.query.get_or_404(req_id)
    data = request.json
    
    try:
        if 'description' in data: req.description = data['description']
        if 'priority' in data: req.priority = data['priority']
        if 'status' in data: req.status = data['status']
        if 'assigned_to' in data: req.assigned_to = data['assigned_to']
        if 'is_approved' in data: req.is_approved = data['is_approved']
        
        db.session.commit()
        return jsonify({"message": "Maintenance request updated"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    status_filter = request.args.get('status')  # Pending | Completed
    q = Task.query.filter_by(deleted_at=None)
    if status_filter:
        q = q.filter_by(status=status_filter)
    tasks = q.order_by(Task.priority.asc()).all()
    return jsonify([{
        "id": t.id,
        "title": t.title,
        "priority": t.priority,
        "status": t.status,
        "service_queue": t.service_queue,
        "proof_url": t.proof_url,
    } for t in tasks]), 200


@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    if not data.get('title'):
        return jsonify({"error": "Task title required"}), 400
    task = Task(
        title=data['title'],
        priority=data.get('priority', 'Medium'),
        status='Pending',
        service_queue=data.get('service_queue'),
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task created", "id": task.id}), 201


@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.json
    task.title = data.get('title', task.title)
    task.priority = data.get('priority', task.priority)
    task.status = data.get('status', task.status)
    task.service_queue = data.get('service_queue', task.service_queue)
    if 'proof_url' in data:
        task.proof_url = data['proof_url']
    db.session.commit()
    return jsonify({"message": "Task updated"}), 200


# ─────── STAFF MANAGEMENT ───────

@tasks_bp.route('/staff', methods=['GET'])
def get_staff():
    staff = StaffMember.query.filter_by(deleted_at=None).all()
    return jsonify([{
        "id": s.id,
        "name": s.name,
        "role": s.role,
        "phone": s.phone,
        "salary": float(s.salary) if s.salary else None,
        "joined_at": s.joined_at.isoformat() if s.joined_at else None,
    } for s in staff]), 200


@tasks_bp.route('/staff', methods=['POST'])
def create_staff():
    data = request.json
    member = StaffMember(
        name=data['name'],
        role=data.get('role', 'Other'),
        phone=data.get('phone'),
        salary=float(data.get('salary', 0)),
        joined_at=datetime.strptime(data['joined_at'], '%Y-%m-%d').date() if data.get('joined_at') else None
    )
    db.session.add(member)
    db.session.commit()
    return jsonify({"message": "Staff member added", "id": member.id}), 201


@tasks_bp.route('/staff/<int:staff_id>', methods=['DELETE'])
def delete_staff(staff_id):
    member = StaffMember.query.get_or_404(staff_id)
    member.delete()
    db.session.commit()
    return jsonify({"message": "Staff removed"}), 200


# ─────── ATTENDANCE ───────

@tasks_bp.route('/staff/attendance', methods=['GET'])
def get_attendance():
    """Get attendance for a date (defaults to today)."""
    date_str = request.args.get('date', date.today().isoformat())
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    staff_list = StaffMember.query.filter_by(deleted_at=None).all()
    result = []
    for s in staff_list:
        record = StaffAttendance.query.filter_by(staff_id=s.id, date=target_date).first()
        result.append({
            "staff_id": s.id,
            "name": s.name,
            "role": s.role,
            "attendance_id": record.id if record else None,
            "status": record.status if record else "Not Marked",
            "time_in": record.time_in if record else None,
            "time_out": record.time_out if record else None,
            "notes": record.notes if record else None,
        })
    return jsonify(result), 200


@tasks_bp.route('/staff/attendance', methods=['POST'])
def mark_attendance():
    data = request.json
    staff_id = data.get('staff_id')
    target_date = datetime.strptime(data.get('date', date.today().isoformat()), '%Y-%m-%d').date()

    existing = StaffAttendance.query.filter_by(staff_id=staff_id, date=target_date).first()
    if existing:
        existing.status = data.get('status', existing.status)
        existing.time_in = data.get('time_in', existing.time_in)
        existing.time_out = data.get('time_out', existing.time_out)
        existing.notes = data.get('notes', existing.notes)
    else:
        record = StaffAttendance(
            staff_id=staff_id,
            date=target_date,
            status=data.get('status', 'Present'),
            time_in=data.get('time_in'),
            time_out=data.get('time_out'),
            notes=data.get('notes'),
        )
        db.session.add(record)

    db.session.commit()
    return jsonify({"message": "Attendance recorded"}), 200
