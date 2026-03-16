"""
backend/routes/moveout.py
Move-Out / Settlement Workflow
"""
from flask import Blueprint, request, jsonify
from backend.models import db, MoveOutRecord, Tenant, Ledger
from datetime import datetime

moveout_bp = Blueprint('moveout', __name__)


@moveout_bp.route('/moveout/<int:tenant_id>', methods=['GET'])
def get_settlement_preview(tenant_id):
    """Preview settlement calculation for a tenant before finalizing."""
    tenant = Tenant.query.get_or_404(tenant_id)

    # Get security deposit from ledger
    deposit = Ledger.query.filter_by(
        tenant_id=tenant_id, type='DEPOSIT', deleted_at=None
    ).first()
    deposit_amount = float(deposit.amount) if deposit else 0

    # Get any unpaid rent from ledger
    unpaid = Ledger.query.filter_by(
        tenant_id=tenant_id, type='RENT', status='PENDING', deleted_at=None
    ).all()
    unpaid_total = sum(float(u.amount) for u in unpaid)

    return jsonify({
        "tenant_id": tenant_id,
        "tenant_name": tenant.name,
        "room": tenant.room.number if tenant.room else "N/A",
        "agreement_start": tenant.agreement_start_date.isoformat() if tenant.agreement_start_date else None,
        "security_deposit_held": deposit_amount,
        "unpaid_rent": unpaid_total,
        "estimated_refund": max(0, deposit_amount - unpaid_total),
    }), 200


@moveout_bp.route('/moveout', methods=['POST'])
def process_moveout():
    """Manager finalizes move-out and calculates final settlement."""
    data = request.json
    tenant_id = data.get('tenant_id')
    if not tenant_id:
        return jsonify({"error": "tenant_id required"}), 400

    tenant = Tenant.query.get_or_404(tenant_id)

    deposit_held = float(data.get('security_deposit_held', 0))
    damage = float(data.get('damage_deduction', 0))
    fines = float(data.get('fine_deduction', 0))
    unpaid = float(data.get('unpaid_rent', 0))
    refund = max(0, deposit_held - damage - fines - unpaid)

    record = MoveOutRecord(
        tenant_id=tenant_id,
        notice_date=datetime.strptime(data['notice_date'], '%Y-%m-%d').date(),
        exit_date=datetime.strptime(data['exit_date'], '%Y-%m-%d').date(),
        security_deposit_held=deposit_held,
        damage_deduction=damage,
        fine_deduction=fines,
        unpaid_rent=unpaid,
        refund_amount=refund,
        notes=data.get('notes', ''),
    )
    db.session.add(record)

    # Soft delete the tenant (preserves history)
    tenant.delete()

    db.session.commit()
    return jsonify({
        "message": "Move-out processed",
        "refund_amount": refund,
        "record_id": record.id
    }), 201


@moveout_bp.route('/moveout', methods=['GET'])
def get_moveout_records():
    """History of all move-outs."""
    records = MoveOutRecord.query.filter_by(deleted_at=None).order_by(MoveOutRecord.created_at.desc()).all()
    return jsonify([{
        "id": r.id,
        "tenant_id": r.tenant_id,
        "notice_date": r.notice_date.isoformat(),
        "exit_date": r.exit_date.isoformat(),
        "security_deposit_held": float(r.security_deposit_held),
        "damage_deduction": float(r.damage_deduction),
        "fine_deduction": float(r.fine_deduction),
        "unpaid_rent": float(r.unpaid_rent),
        "refund_amount": float(r.refund_amount),
        "notes": r.notes,
    } for r in records]), 200
