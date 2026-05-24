from datetime import datetime, date


def format_date(dt):
    if isinstance(dt, datetime):
        return dt.strftime('%d-%m-%Y')
    if isinstance(dt, date):
        return dt.strftime('%d-%m-%Y')
    return str(dt)


def format_datetime(dt):
    if isinstance(dt, datetime):
        return dt.strftime('%d-%m-%Y %I:%M %p')
    return str(dt)


def format_currency(amount):
    try:
        return f'{float(amount):,.2f}'
    except (ValueError, TypeError):
        return '0.00'


def calculate_outstanding(opening_balance, total_invoices, total_payments):
    return opening_balance + total_invoices - total_payments


def get_payment_modes():
    return ['Cash', 'Cheque', 'Bank Transfer', 'Online', 'UPI', 'Card', 'Other']
