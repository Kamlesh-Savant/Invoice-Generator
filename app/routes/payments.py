from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app import db
from app.models.party import Party
from app.models.payment import Payment
from app.models.setting import Setting
from datetime import datetime

payments_bp = Blueprint('payments', __name__, url_prefix='/payments')


def generate_payment_number():
    prefix = Setting.get('payment_prefix', 'PAY-')
    last = Payment.query.order_by(Payment.id.desc()).first()
    if last:
        try:
            num = int(last.payment_number.replace(prefix, '')) + 1
        except ValueError:
            num = 1
    else:
        num = 1
    return f'{prefix}{num:05d}'


@payments_bp.route('/')
@login_required
def index():
    search = request.args.get('search', '').strip()
    party_id = request.args.get('party_id', type=int)
    payment_mode = request.args.get('payment_mode', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    page = request.args.get('page', 1, type=int)
    per_page = 20

    query = Payment.query

    if search:
        query = query.filter(Payment.payment_number.ilike(f'%{search}%'))

    if party_id:
        query = query.filter(Payment.party_id == party_id)

    if payment_mode:
        query = query.filter(Payment.payment_mode == payment_mode)

    if date_from:
        try:
            dt = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(Payment.payment_date >= dt)
        except ValueError:
            pass

    if date_to:
        try:
            dt = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(Payment.payment_date <= dt)
        except ValueError:
            pass

    query = query.order_by(Payment.payment_date.desc(), Payment.id.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    payments = pagination.items

    parties = Party.query.order_by(Party.party_name).all()
    payment_modes = ['Cash', 'Cheque', 'Bank Transfer', 'Online', 'UPI', 'Card', 'Other']

    return render_template(
        'payments/index.html',
        payments=payments,
        pagination=pagination,
        search=search,
        party_id=party_id,
        payment_mode=payment_mode,
        date_from=date_from,
        date_to=date_to,
        parties=parties,
        payment_modes=payment_modes
    )


@payments_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        party_id = request.form.get('party_id', type=int)
        payment_date = request.form.get('payment_date', datetime.now().strftime('%Y-%m-%d'))
        payment_mode = request.form.get('payment_mode', 'Cash')
        amount = request.form.get('amount', 0)
        reference_number = request.form.get('reference_number', '').strip()
        notes = request.form.get('notes', '').strip()

        if not party_id:
            flash('Please select a party.', 'warning')
            parties = Party.query.order_by(Party.party_name).all()
            payment_modes = ['Cash', 'Cheque', 'Bank Transfer', 'Online', 'UPI', 'Card', 'Other']
            return render_template('payments/form.html', payment=None, parties=parties, payment_modes=payment_modes, title='Record Payment')

        party = Party.query.get(party_id)
        if not party:
            flash('Selected party not found.', 'danger')
            return redirect(url_for('payments.add'))

        try:
            amount = float(amount) if amount else 0
        except ValueError:
            amount = 0

        if amount <= 0:
            flash('Amount must be greater than zero.', 'warning')
            parties = Party.query.order_by(Party.party_name).all()
            payment_modes = ['Cash', 'Cheque', 'Bank Transfer', 'Online', 'UPI', 'Card', 'Other']
            return render_template('payments/form.html', payment=None, parties=parties, payment_modes=payment_modes, title='Record Payment')

        try:
            payment_date = datetime.strptime(payment_date, '%Y-%m-%d').date()
        except ValueError:
            payment_date = datetime.now().date()

        payment_number = generate_payment_number()
        payment = Payment(
            payment_number=payment_number,
            payment_date=payment_date,
            party_id=party_id,
            payment_mode=payment_mode,
            amount=amount,
            reference_number=reference_number,
            notes=notes
        )
        db.session.add(payment)
        db.session.commit()
        flash(f'Payment {payment_number} of {amount:.2f} recorded successfully.', 'success')
        return redirect(url_for('payments.index'))

    parties = Party.query.order_by(Party.party_name).all()
    payment_modes = ['Cash', 'Cheque', 'Bank Transfer', 'Online', 'UPI', 'Card', 'Other']
    return render_template('payments/form.html', payment=None, parties=parties, payment_modes=payment_modes, title='Record Payment')


@payments_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    payment = Payment.query.get_or_404(id)

    if request.method == 'POST':
        party_id = request.form.get('party_id', type=int)
        payment_date = request.form.get('payment_date', '')
        payment_mode = request.form.get('payment_mode', 'Cash')
        amount = request.form.get('amount', 0)
        reference_number = request.form.get('reference_number', '').strip()
        notes = request.form.get('notes', '').strip()

        if not party_id:
            flash('Please select a party.', 'warning')
            parties = Party.query.order_by(Party.party_name).all()
            payment_modes = ['Cash', 'Cheque', 'Bank Transfer', 'Online', 'UPI', 'Card', 'Other']
            return render_template('payments/form.html', payment=payment, parties=parties, payment_modes=payment_modes, title='Edit Payment')

        try:
            amount = float(amount) if amount else 0
        except ValueError:
            amount = 0

        if amount <= 0:
            flash('Amount must be greater than zero.', 'warning')
            parties = Party.query.order_by(Party.party_name).all()
            payment_modes = ['Cash', 'Cheque', 'Bank Transfer', 'Online', 'UPI', 'Card', 'Other']
            return render_template('payments/form.html', payment=payment, parties=parties, payment_modes=payment_modes, title='Edit Payment')

        try:
            payment_date = datetime.strptime(payment_date, '%Y-%m-%d').date()
        except ValueError:
            payment_date = payment.payment_date

        payment.party_id = party_id
        payment.payment_date = payment_date
        payment.payment_mode = payment_mode
        payment.amount = amount
        payment.reference_number = reference_number
        payment.notes = notes
        db.session.commit()
        flash(f'Payment {payment.payment_number} updated successfully.', 'success')
        return redirect(url_for('payments.index'))

    parties = Party.query.order_by(Party.party_name).all()
    payment_modes = ['Cash', 'Cheque', 'Bank Transfer', 'Online', 'UPI', 'Card', 'Other']
    return render_template('payments/form.html', payment=payment, parties=parties, payment_modes=payment_modes, title='Edit Payment')


@payments_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    payment = Payment.query.get_or_404(id)
    num = payment.payment_number
    db.session.delete(payment)
    db.session.commit()
    flash(f'Payment {num} deleted successfully.', 'success')
    return redirect(url_for('payments.index'))


@payments_bp.route('/view/<int:id>')
@login_required
def view(id):
    payment = Payment.query.get_or_404(id)
    return render_template('payments/view.html', payment=payment)
