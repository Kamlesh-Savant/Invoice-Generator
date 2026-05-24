from flask import Blueprint, render_template
from flask_login import login_required
from app import db
from app.models.party import Party
from app.models.invoice import Invoice
from app.models.payment import Payment
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/')


@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    total_parties = Party.query.count()
    total_invoices = Invoice.query.count()
    total_payments = Payment.query.count()

    total_invoice_amount = db.session.query(func.coalesce(func.sum(Invoice.total_amount), 0)).scalar()
    total_payment_amount = db.session.query(func.coalesce(func.sum(Payment.amount), 0)).scalar()

    recent_invoices = Invoice.query.order_by(Invoice.created_at.desc()).limit(5).all()
    recent_payments = Payment.query.order_by(Payment.created_at.desc()).limit(5).all()

    parties_outstanding = []
    parties = Party.query.order_by(Party.party_name).all()
    for party in parties:
        outstanding = party.outstanding()
        if outstanding != 0:
            parties_outstanding.append({
                'id': party.id,
                'name': party.party_name,
                'outstanding': outstanding
            })

    parties_outstanding.sort(key=lambda x: abs(x['outstanding']), reverse=True)
    parties_outstanding = parties_outstanding[:10]

    return render_template(
        'dashboard/index.html',
        total_parties=total_parties,
        total_invoices=total_invoices,
        total_payments=total_payments,
        total_invoice_amount=total_invoice_amount,
        total_payment_amount=total_payment_amount,
        recent_invoices=recent_invoices,
        recent_payments=recent_payments,
        parties_outstanding=parties_outstanding
    )
