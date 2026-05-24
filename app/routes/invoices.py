from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app import db
from app.models.party import Party
from app.models.invoice import Invoice, InvoiceItem
from app.models.setting import Setting
from datetime import datetime

invoices_bp = Blueprint('invoices', __name__, url_prefix='/invoices')


def generate_invoice_number():
    prefix = Setting.get('invoice_prefix', 'INV-')
    last = Invoice.query.order_by(Invoice.id.desc()).first()
    if last:
        try:
            num = int(last.invoice_number.replace(prefix, '')) + 1
        except ValueError:
            num = 1
    else:
        num = 1
    return f'{prefix}{num:05d}'


@invoices_bp.route('/')
@login_required
def index():
    search = request.args.get('search', '').strip()
    party_id = request.args.get('party_id', type=int)
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    page = request.args.get('page', 1, type=int)
    per_page = 20

    query = Invoice.query

    if search:
        query = query.filter(Invoice.invoice_number.ilike(f'%{search}%'))

    if party_id:
        query = query.filter(Invoice.party_id == party_id)

    if date_from:
        try:
            dt = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(Invoice.invoice_date >= dt)
        except ValueError:
            pass

    if date_to:
        try:
            dt = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(Invoice.invoice_date <= dt)
        except ValueError:
            pass

    query = query.order_by(Invoice.invoice_date.desc(), Invoice.id.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    invoices = pagination.items

    parties = Party.query.order_by(Party.party_name).all()

    return render_template(
        'invoices/index.html',
        invoices=invoices,
        pagination=pagination,
        search=search,
        party_id=party_id,
        date_from=date_from,
        date_to=date_to,
        parties=parties
    )


@invoices_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        party_id = request.form.get('party_id', type=int)
        invoice_date = request.form.get('invoice_date', datetime.now().strftime('%Y-%m-%d'))
        notes = request.form.get('notes', '').strip()

        if not party_id:
            flash('Please select a party.', 'warning')
            parties = Party.query.order_by(Party.party_name).all()
            return render_template('invoices/form.html', invoice=None, parties=parties, items=[], title='Create Invoice')

        party = Party.query.get(party_id)
        if not party:
            flash('Selected party not found.', 'danger')
            return redirect(url_for('invoices.add'))

        try:
            invoice_date = datetime.strptime(invoice_date, '%Y-%m-%d').date()
        except ValueError:
            invoice_date = datetime.now().date()

        invoice_number = generate_invoice_number()
        invoice = Invoice(
            invoice_number=invoice_number,
            invoice_date=invoice_date,
            party_id=party_id,
            notes=notes
        )
        db.session.add(invoice)
        db.session.flush()

        product_names = request.form.getlist('product_name[]')
        quantities = request.form.getlist('quantity[]')
        rates = request.form.getlist('rate[]')

        subtotal = 0.0
        for i in range(len(product_names)):
            name = product_names[i].strip()
            if not name:
                continue
            try:
                qty = float(quantities[i]) if quantities[i] else 0
            except ValueError:
                qty = 0
            try:
                rate = float(rates[i]) if rates[i] else 0
            except ValueError:
                rate = 0
            amount = qty * rate
            if amount == 0:
                continue
            item = InvoiceItem(
                invoice_id=invoice.id,
                product_name=name,
                quantity=qty,
                rate=rate,
                amount=amount
            )
            db.session.add(item)
            subtotal += amount

        if subtotal == 0:
            db.session.rollback()
            flash('Please add at least one item with valid quantity and rate.', 'warning')
            parties = Party.query.order_by(Party.party_name).all()
            return render_template('invoices/form.html', invoice=None, parties=parties, items=[], title='Create Invoice')

        invoice.subtotal = subtotal
        invoice.total_amount = subtotal
        db.session.commit()
        flash(f'Invoice {invoice.invoice_number} created successfully.', 'success')
        return redirect(url_for('invoices.index'))

    parties = Party.query.order_by(Party.party_name).all()
    return render_template('invoices/form.html', invoice=None, parties=parties, items=[], title='Create Invoice')


@invoices_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    invoice = Invoice.query.get_or_404(id)

    if request.method == 'POST':
        party_id = request.form.get('party_id', type=int)
        invoice_date = request.form.get('invoice_date', '')
        notes = request.form.get('notes', '').strip()

        if not party_id:
            flash('Please select a party.', 'warning')
            parties = Party.query.order_by(Party.party_name).all()
            return render_template('invoices/form.html', invoice=invoice, parties=parties, title='Edit Invoice')

        party = Party.query.get(party_id)
        if not party:
            flash('Selected party not found.', 'danger')
            return redirect(url_for('invoices.edit', id=id))

        try:
            invoice_date = datetime.strptime(invoice_date, '%Y-%m-%d').date()
        except ValueError:
            invoice_date = invoice.invoice_date

        invoice.party_id = party_id
        invoice.invoice_date = invoice_date
        invoice.notes = notes

        InvoiceItem.query.filter_by(invoice_id=invoice.id).delete()

        product_names = request.form.getlist('product_name[]')
        quantities = request.form.getlist('quantity[]')
        rates = request.form.getlist('rate[]')

        subtotal = 0.0
        for i in range(len(product_names)):
            name = product_names[i].strip()
            if not name:
                continue
            try:
                qty = float(quantities[i]) if quantities[i] else 0
            except ValueError:
                qty = 0
            try:
                rate = float(rates[i]) if rates[i] else 0
            except ValueError:
                rate = 0
            amount = qty * rate
            if amount == 0:
                continue
            item = InvoiceItem(
                invoice_id=invoice.id,
                product_name=name,
                quantity=qty,
                rate=rate,
                amount=amount
            )
            db.session.add(item)
            subtotal += amount

        if subtotal == 0:
            db.session.rollback()
            flash('Please add at least one item with valid quantity and rate.', 'warning')
            parties = Party.query.order_by(Party.party_name).all()
            items = invoice.items
            return render_template('invoices/form.html', invoice=invoice, parties=parties, items=items, title='Edit Invoice')

        invoice.subtotal = subtotal
        invoice.total_amount = subtotal
        db.session.commit()
        flash(f'Invoice {invoice.invoice_number} updated successfully.', 'success')
        return redirect(url_for('invoices.index'))

    parties = Party.query.order_by(Party.party_name).all()
    items = invoice.items
    return render_template('invoices/form.html', invoice=invoice, parties=parties, items=items, title='Edit Invoice')


@invoices_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    invoice = Invoice.query.get_or_404(id)
    num = invoice.invoice_number
    db.session.delete(invoice)
    db.session.commit()
    flash(f'Invoice {num} deleted successfully.', 'success')
    return redirect(url_for('invoices.index'))


@invoices_bp.route('/view/<int:id>')
@login_required
def view(id):
    invoice = Invoice.query.get_or_404(id)
    return render_template('invoices/view.html', invoice=invoice)
