from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app import db
from app.models.party import Party
from app.models.invoice import Invoice
from app.models.payment import Payment
from datetime import datetime, date
from sqlalchemy import func, or_

ledger_bp = Blueprint('ledger', __name__, url_prefix='/ledger')


def get_ledger_entries(party_id=None, date_from=None, date_to=None):
    entries = []

    opening_balance = 0.0

    if party_id:
        party = Party.query.get(party_id)
        if not party:
            return entries, 0, 0
        opening_balance = party.opening_balance

    invoice_query = db.session.query(
        Invoice.invoice_date.label('entry_date'),
        db.literal('Invoice').label('entry_type'),
        Invoice.invoice_number.label('ref_number'),
        Invoice.total_amount.label('debit'),
        db.literal(0.0).label('credit'),
        Invoice.party_id,
        Invoice.id.label('ref_id'),
        Invoice.party_id.label('filter_party_id')
    )

    payment_query = db.session.query(
        Payment.payment_date.label('entry_date'),
        db.literal('Payment').label('entry_type'),
        Payment.payment_number.label('ref_number'),
        db.literal(0.0).label('debit'),
        Payment.amount.label('credit'),
        Payment.party_id,
        Payment.id.label('ref_id'),
        Payment.party_id.label('filter_party_id')
    )

    if party_id:
        invoice_query = invoice_query.filter(Invoice.party_id == party_id)
        payment_query = payment_query.filter(Payment.party_id == party_id)

    if date_from:
        invoice_query = invoice_query.filter(Invoice.invoice_date >= date_from)
        payment_query = payment_query.filter(Payment.payment_date >= date_from)

    if date_to:
        invoice_query = invoice_query.filter(Invoice.invoice_date <= date_to)
        payment_query = payment_query.filter(Payment.payment_date <= date_to)

    invoices = invoice_query.all()
    payments = payment_query.all()

    all_entries = []

    for inv in invoices:
        all_entries.append({
            'date': inv.entry_date,
            'type': 'Invoice',
            'ref_number': inv.ref_number,
            'debit': inv.debit,
            'credit': inv.credit,
            'party_id': inv.filter_party_id,
            'ref_id': inv.ref_id
        })

    for pay in payments:
        all_entries.append({
            'date': pay.entry_date,
            'type': 'Payment',
            'ref_number': pay.ref_number,
            'debit': pay.debit,
            'credit': pay.credit,
            'party_id': pay.filter_party_id,
            'ref_id': pay.ref_id
        })

    all_entries.sort(key=lambda x: (x['date'], x['type'] != 'Invoice', x['ref_number']))

    running_balance = opening_balance
    for entry in all_entries:
        running_balance += entry['debit'] - entry['credit']
        entry['balance'] = running_balance

    return all_entries, opening_balance, running_balance


@ledger_bp.route('/')
@login_required
def index():
    party_id = request.args.get('party_id', type=int)
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    page = request.args.get('page', 1, type=int)
    per_page = 50

    parsed_date_from = None
    parsed_date_to = None

    if date_from:
        try:
            parsed_date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
        except ValueError:
            parsed_date_from = None

    if date_to:
        try:
            parsed_date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        except ValueError:
            parsed_date_to = None

    if party_id:
        entries, opening_bal, closing_bal = get_ledger_entries(
            party_id=party_id,
            date_from=parsed_date_from,
            date_to=parsed_date_to
        )

        total_entries = len(entries)
        total_pages = max(1, (total_entries + per_page - 1) // per_page)
        start = (page - 1) * per_page
        end = start + per_page
        page_entries = entries[start:end]

        party = Party.query.get(party_id)
        party_name = party.party_name if party else ''
    else:
        entries = []
        page_entries = []
        total_pages = 1
        opening_bal = 0
        closing_bal = 0
        party_name = ''

    parties = Party.query.order_by(Party.party_name).all()

    return render_template(
        'ledger/index.html',
        entries=page_entries,
        all_entries=entries,
        pagination=None,
        page=page,
        total_pages=total_pages,
        party_id=party_id,
        party_name=party_name,
        date_from=date_from,
        date_to=date_to,
        opening_balance=opening_bal,
        closing_balance=closing_bal,
        parties=parties
    )


@ledger_bp.route('/party/<int:party_id>')
@login_required
def party_ledger(party_id):
    party = Party.query.get_or_404(party_id)
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    page = request.args.get('page', 1, type=int)
    per_page = 50

    parsed_date_from = None
    parsed_date_to = None

    if date_from:
        try:
            parsed_date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
        except ValueError:
            parsed_date_from = None

    if date_to:
        try:
            parsed_date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        except ValueError:
            parsed_date_to = None

    entries, opening_bal, closing_bal = get_ledger_entries(
        party_id=party_id,
        date_from=parsed_date_from,
        date_to=parsed_date_to
    )

    total_entries = len(entries)
    total_pages = max(1, (total_entries + per_page - 1) // per_page)
    start = (page - 1) * per_page
    end = start + per_page
    page_entries = entries[start:end]

    return render_template(
        'ledger/party_ledger.html',
        entries=page_entries,
        all_entries=entries,
        party=party,
        page=page,
        total_pages=total_pages,
        date_from=date_from,
        date_to=date_to,
        opening_balance=opening_bal,
        closing_balance=closing_bal
    )


@ledger_bp.route('/combined')
@login_required
def combined():
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    page = request.args.get('page', 1, type=int)
    per_page = 50

    parsed_date_from = None
    parsed_date_to = None

    if date_from:
        try:
            parsed_date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
        except ValueError:
            parsed_date_from = None

    if date_to:
        try:
            parsed_date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        except ValueError:
            parsed_date_to = None

    parties = Party.query.order_by(Party.party_name).all()
    combined_data = []

    for party in parties:
        entries, opening_bal, closing_bal = get_ledger_entries(
            party_id=party.id,
            date_from=parsed_date_from,
            date_to=parsed_date_to
        )
        outstanding = party.outstanding()
        combined_data.append({
            'party': party,
            'opening_balance': opening_bal,
            'total_invoices': sum(e['debit'] for e in entries),
            'total_payments': sum(e['credit'] for e in entries),
            'closing_balance': closing_bal,
            'outstanding': outstanding
        })

    return render_template(
        'ledger/combined.html',
        combined_data=combined_data,
        date_from=date_from,
        date_to=date_to
    )
