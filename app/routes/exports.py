from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from flask_login import login_required
from app.models.party import Party
from app.models.invoice import Invoice, InvoiceItem
from app.models.payment import Payment
from app.models.setting import Setting
from app.routes.ledger import get_ledger_entries
from datetime import datetime
import io
import os

exports_bp = Blueprint('exports', __name__, url_prefix='/exports')


@exports_bp.route('/invoice/pdf/<int:invoice_id>')
@login_required
def invoice_pdf(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    business_name = Setting.get('business_name', 'My Business')
    business_address = Setting.get('business_address', '')
    business_mobile = Setting.get('business_mobile', '')
    business_email = Setting.get('business_email', '')
    business_gst = Setting.get('business_gst', '')

    try:
        from app.services.pdf_generator import generate_invoice_pdf
        pdf_bytes = generate_invoice_pdf(
            invoice=invoice,
            business_name=business_name,
            business_address=business_address,
            business_mobile=business_mobile,
            business_email=business_email,
            business_gst=business_gst
        )
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'invoice_{invoice.invoice_number}.pdf'
        )
    except ImportError:
        flash('PDF generation module not available. Install reportlab.', 'warning')
        return redirect(url_for('invoices.view', id=invoice_id))
    except Exception as e:
        flash(f'Error generating PDF: {str(e)}', 'danger')
        return redirect(url_for('invoices.view', id=invoice_id))


@exports_bp.route('/payment/pdf/<int:payment_id>')
@login_required
def payment_pdf(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    business_name = Setting.get('business_name', 'My Business')

    try:
        from app.services.pdf_generator import generate_payment_pdf
        pdf_bytes = generate_payment_pdf(payment=payment, business_name=business_name)
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'payment_{payment.payment_number}.pdf'
        )
    except ImportError:
        flash('PDF generation module not available.', 'warning')
        return redirect(url_for('payments.view', id=payment_id))
    except Exception as e:
        flash(f'Error generating PDF: {str(e)}', 'danger')
        return redirect(url_for('payments.view', id=payment_id))


@exports_bp.route('/ledger/pdf')
@login_required
def ledger_pdf():
    party_id = request.args.get('party_id', type=int)
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')

    parsed_date_from = None
    parsed_date_to = None

    if date_from:
        try:
            parsed_date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
        except ValueError:
            pass

    if date_to:
        try:
            parsed_date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        except ValueError:
            pass

    entries, opening_bal, closing_bal = get_ledger_entries(
        party_id=party_id,
        date_from=parsed_date_from,
        date_to=parsed_date_to
    )

    party_name = ''
    if party_id:
        party = Party.query.get(party_id)
        party_name = party.party_name if party else ''

    business_name = Setting.get('business_name', 'My Business')

    try:
        from app.services.pdf_generator import generate_ledger_pdf
        pdf_bytes = generate_ledger_pdf(
            entries=entries,
            party_name=party_name,
            business_name=business_name,
            opening_balance=opening_bal,
            closing_balance=closing_bal,
            date_from=date_from,
            date_to=date_to
        )
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='ledger_statement.pdf'
        )
    except ImportError:
        flash('PDF generation module not available.', 'warning')
        return redirect(url_for('ledger.index'))
    except Exception as e:
        flash(f'Error generating PDF: {str(e)}', 'danger')
        return redirect(url_for('ledger.index'))


@exports_bp.route('/ledger/excel')
@login_required
def ledger_excel():
    party_id = request.args.get('party_id', type=int)
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')

    parsed_date_from = None
    parsed_date_to = None

    if date_from:
        try:
            parsed_date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
        except ValueError:
            pass

    if date_to:
        try:
            parsed_date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        except ValueError:
            pass

    entries, opening_bal, closing_bal = get_ledger_entries(
        party_id=party_id,
        date_from=parsed_date_from,
        date_to=parsed_date_to
    )

    party_name = ''
    if party_id:
        party = Party.query.get(party_id)
        party_name = party.party_name if party else ''

    business_name = Setting.get('business_name', 'My Business')

    try:
        from app.services.excel_generator import generate_ledger_excel
        excel_bytes = generate_ledger_excel(
            entries=entries,
            party_name=party_name,
            business_name=business_name,
            opening_balance=opening_bal,
            closing_balance=closing_bal,
            date_from=date_from,
            date_to=date_to
        )
        return send_file(
            io.BytesIO(excel_bytes),
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='ledger_statement.xlsx'
        )
    except ImportError:
        flash('Excel generation module not available. Install openpyxl.', 'warning')
        return redirect(url_for('ledger.index'))
    except Exception as e:
        flash(f'Error generating Excel: {str(e)}', 'danger')
        return redirect(url_for('ledger.index'))


@exports_bp.route('/party/statement/excel/<int:party_id>')
@login_required
def party_statement_excel(party_id):
    party = Party.query.get_or_404(party_id)
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')

    parsed_date_from = None
    parsed_date_to = None

    if date_from:
        try:
            parsed_date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
        except ValueError:
            pass

    if date_to:
        try:
            parsed_date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        except ValueError:
            pass

    entries, opening_bal, closing_bal = get_ledger_entries(
        party_id=party_id,
        date_from=parsed_date_from,
        date_to=parsed_date_to
    )

    business_name = Setting.get('business_name', 'My Business')

    try:
        from app.services.excel_generator import generate_ledger_excel
        excel_bytes = generate_ledger_excel(
            entries=entries,
            party_name=party.party_name,
            business_name=business_name,
            opening_balance=opening_bal,
            closing_balance=closing_bal,
            date_from=date_from,
            date_to=date_to
        )
        return send_file(
            io.BytesIO(excel_bytes),
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'statement_{party.party_name}.xlsx'
        )
    except ImportError:
        flash('Excel generation module not available. Install openpyxl.', 'warning')
        return redirect(url_for('ledger.party_ledger', party_id=party_id))
    except Exception as e:
        flash(f'Error generating Excel: {str(e)}', 'danger')
        return redirect(url_for('ledger.party_ledger', party_id=party_id))
