from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.platypus.flowables import HRFlowable
from io import BytesIO
from datetime import datetime


def _draw_background(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor('#f8f9fa'))
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.restoreState()


def generate_invoice_pdf(invoice, business_name='My Business', business_address='',
                         business_mobile='', business_email='', business_gst=''):
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        topMargin=15*mm, bottomMargin=15*mm,
        leftMargin=15*mm, rightMargin=15*mm
    )

    styles = getSampleStyleSheet()
    style_normal = styles['Normal']
    style_heading = styles['Heading1']
    style_title = styles['Title']

    elements = []

    elements.append(Paragraph(
        business_name.upper(),
        ParagraphStyle('BusinessName', parent=style_title, fontSize=18, spaceAfter=4,
                       textColor=colors.HexColor('#1a237e'))
    ))
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1a237e')))
    elements.append(Spacer(1, 6))

    if business_address:
        elements.append(Paragraph(business_address, style_normal))
    if business_mobile:
        elements.append(Paragraph(f'Mobile: {business_mobile}', style_normal))
    if business_email:
        elements.append(Paragraph(f'Email: {business_email}', style_normal))
    if business_gst:
        elements.append(Paragraph(f'GST: {business_gst}', style_normal))

    elements.append(Spacer(1, 10))

    elements.append(Paragraph(
        'TAX INVOICE',
        ParagraphStyle('InvoiceTitle', parent=style_heading, fontSize=16, alignment=1,
                       spaceAfter=10, textColor=colors.HexColor('#1a237e'))
    ))

    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cccccc')))
    elements.append(Spacer(1, 8))

    party = invoice.party
    invoice_info = [
        [Paragraph(f'<b>Invoice No:</b> {invoice.invoice_number}', style_normal),
         Paragraph(f'<b>Date:</b> {invoice.invoice_date.strftime("%d-%m-%Y")}', style_normal)],
    ]
    if party:
        invoice_info.append([
            Paragraph(f'<b>Party:</b> {party.party_name}', style_normal),
            Paragraph(f'<b>Mobile:</b> {party.mobile or "-"}', style_normal)
        ])
        invoice_info.append([
            Paragraph(f'<b>Address:</b> {party.address or "-"}', style_normal),
            Paragraph(f'<b>Email:</b> {party.email or "-"}', style_normal)
        ])

    info_table = Table(invoice_info, colWidths=[doc.width * 0.5, doc.width * 0.5])
    info_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 10))

    items_data = [
        [Paragraph('<b>#</b>', style_normal),
         Paragraph('<b>Product</b>', style_normal),
         Paragraph('<b>Qty</b>', style_normal),
         Paragraph('<b>Rate</b>', style_normal),
         Paragraph('<b>Amount</b>', style_normal)]
    ]

    for idx, item in enumerate(invoice.items, 1):
        items_data.append([
            Paragraph(str(idx), style_normal),
            Paragraph(item.product_name, style_normal),
            Paragraph(str(item.quantity), style_normal),
            Paragraph(f'{item.rate:.2f}', style_normal),
            Paragraph(f'{item.amount:.2f}', style_normal)
        ])

    col_widths = [30, doc.width * 0.4, 60, 80, 90]
    items_table = Table(items_data, colWidths=col_widths, repeatRows=1)
    items_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#999999')),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fafafa')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#fafafa'), colors.white]),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 10))

    total_data = [
        [Paragraph('<b>Total Amount</b>', ParagraphStyle('TotalLabel', parent=style_normal, fontSize=12)),
         Paragraph(f'<b>Rs. {invoice.total_amount:.2f}</b>',
                   ParagraphStyle('TotalValue', parent=style_normal, fontSize=12, alignment=2))]
    ]
    total_table = Table(total_data, colWidths=[doc.width * 0.7, doc.width * 0.3])
    total_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#1a237e')),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#1a237e')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8eaf6')),
    ]))
    elements.append(total_table)

    if invoice.notes:
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f'<b>Notes:</b> {invoice.notes}', style_normal))

    elements.append(Spacer(1, 20))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cccccc')))
    elements.append(Paragraph(
        'This is a computer-generated invoice.',
        ParagraphStyle('Footer', parent=style_normal, fontSize=8, textColor=colors.gray, alignment=1)
    ))

    doc.build(elements, onFirstPage=_draw_background, onLaterPages=_draw_background)
    return buf.getvalue()


def generate_payment_pdf(payment, business_name='My Business'):
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        topMargin=15*mm, bottomMargin=15*mm,
        leftMargin=15*mm, rightMargin=15*mm
    )

    styles = getSampleStyleSheet()
    style_normal = styles['Normal']
    style_heading = styles['Heading1']
    style_title = styles['Title']

    elements = []

    elements.append(Paragraph(
        business_name.upper(),
        ParagraphStyle('BusinessName', parent=style_title, fontSize=18, spaceAfter=4,
                       textColor=colors.HexColor('#1a237e'))
    ))
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1a237e')))
    elements.append(Spacer(1, 6))

    elements.append(Paragraph(
        'PAYMENT RECEIPT',
        ParagraphStyle('ReceiptTitle', parent=style_heading, fontSize=16, alignment=1,
                       spaceAfter=10, textColor=colors.HexColor('#1a237e'))
    ))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cccccc')))
    elements.append(Spacer(1, 8))

    party = payment.party
    data = [
        [Paragraph('<b>Payment No:</b>', style_normal), Paragraph(payment.payment_number, style_normal),
         Paragraph('<b>Date:</b>', style_normal), Paragraph(payment.payment_date.strftime('%d-%m-%Y'), style_normal)],
        [Paragraph('<b>Party:</b>', style_normal), Paragraph(party.party_name if party else '-', style_normal),
         Paragraph('<b>Mode:</b>', style_normal), Paragraph(payment.payment_mode, style_normal)],
        [Paragraph('<b>Amount:</b>', style_normal),
         Paragraph(f'<b>Rs. {payment.amount:.2f}</b>', ParagraphStyle('Amount', parent=style_normal, fontSize=12)),
         Paragraph('<b>Ref No:</b>', style_normal), Paragraph(payment.reference_number or '-', style_normal)],
    ]

    info_table = Table(data, colWidths=[doc.width * 0.15, doc.width * 0.35, doc.width * 0.15, doc.width * 0.35])
    info_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f5f5f5')),
        ('BACKGROUND', (0, 2), (0, 2), colors.HexColor('#e8eaf6')),
    ]))
    elements.append(info_table)

    if payment.notes:
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f'<b>Notes:</b> {payment.notes}', style_normal))

    elements.append(Spacer(1, 20))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cccccc')))
    elements.append(Paragraph(
        'This is a computer-generated receipt.',
        ParagraphStyle('Footer', parent=style_normal, fontSize=8, textColor=colors.gray, alignment=1)
    ))

    doc.build(elements, onFirstPage=_draw_background, onLaterPages=_draw_background)
    return buf.getvalue()


def generate_ledger_pdf(entries, party_name='', business_name='My Business',
                        opening_balance=0, closing_balance=0,
                        date_from='', date_to=''):
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        topMargin=15*mm, bottomMargin=15*mm,
        leftMargin=12*mm, rightMargin=12*mm
    )

    styles = getSampleStyleSheet()
    style_normal = styles['Normal']
    style_heading = styles['Heading1']
    style_title = styles['Title']

    elements = []

    elements.append(Paragraph(
        business_name.upper(),
        ParagraphStyle('BusinessName', parent=style_title, fontSize=16, spaceAfter=4,
                       textColor=colors.HexColor('#1a237e'))
    ))
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1a237e')))
    elements.append(Spacer(1, 4))

    title = 'LEDGER STATEMENT'
    if party_name:
        title += f' - {party_name.upper()}'
    elements.append(Paragraph(
        title,
        ParagraphStyle('LedgerTitle', parent=style_heading, fontSize=13, spaceAfter=4,
                       textColor=colors.HexColor('#1a237e'))
    ))

    if date_from or date_to:
        date_range = f'Period: {date_from} to {date_to}' if date_from and date_to else f'From: {date_from or "Start"} To: {date_to or "End"}'
        elements.append(Paragraph(date_range, ParagraphStyle('DateRange', parent=style_normal, fontSize=8, textColor=colors.gray)))
    elements.append(Spacer(1, 6))

    header_row = [
        Paragraph('<b>Date</b>', style_normal),
        Paragraph('<b>Type</b>', style_normal),
        Paragraph('<b>Ref No</b>', style_normal),
        Paragraph('<b>Debit</b>', style_normal),
        Paragraph('<b>Credit</b>', style_normal),
        Paragraph('<b>Balance</b>', style_normal),
    ]

    table_data = [header_row]

    table_data.append([
        Paragraph('Opening Balance', ParagraphStyle('Opening', parent=style_normal, fontSize=7)),
        Paragraph('', style_normal),
        Paragraph('', style_normal),
        Paragraph('', style_normal),
        Paragraph('', style_normal),
        Paragraph(f'{opening_balance:.2f}', ParagraphStyle('Bal', parent=style_normal, fontSize=7, alignment=2))
    ])

    for entry in entries:
        bal_color = colors.HexColor('#1b5e20') if entry['balance'] >= 0 else colors.HexColor('#b71c1c')
        entry_type_color = colors.HexColor('#1565c0') if entry['type'] == 'Invoice' else colors.HexColor('#e65100')
        table_data.append([
            Paragraph(entry['date'].strftime('%d-%m-%Y') if hasattr(entry['date'], 'strftime') else str(entry['date']),
                      ParagraphStyle('Date', parent=style_normal, fontSize=7)),
            Paragraph(entry['type'],
                      ParagraphStyle('Type', parent=style_normal, fontSize=7, textColor=entry_type_color)),
            Paragraph(entry['ref_number'],
                      ParagraphStyle('Ref', parent=style_normal, fontSize=7)),
            Paragraph(f'{entry["debit"]:.2f}' if entry['debit'] > 0 else '',
                      ParagraphStyle('Debit', parent=style_normal, fontSize=7, alignment=2)),
            Paragraph(f'{entry["credit"]:.2f}' if entry['credit'] > 0 else '',
                      ParagraphStyle('Credit', parent=style_normal, fontSize=7, alignment=2)),
            Paragraph(f'{entry["balance"]:.2f}',
                      ParagraphStyle('Balance', parent=style_normal, fontSize=7, alignment=2, textColor=bal_color))
        ])

    table_data.append([
        Paragraph('<b>Closing Balance</b>', ParagraphStyle('Closing', parent=style_normal, fontSize=8)),
        Paragraph('', style_normal),
        Paragraph('', style_normal),
        Paragraph('', style_normal),
        Paragraph('', style_normal),
        Paragraph(f'<b>{closing_balance:.2f}</b>',
                  ParagraphStyle('ClosingBal', parent=style_normal, fontSize=8, alignment=2))
    ])

    col_widths = [doc.width * 0.14, doc.width * 0.12, doc.width * 0.22, doc.width * 0.16, doc.width * 0.16, doc.width * 0.20]
    table = Table(table_data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#cccccc')),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#e8eaf6')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8eaf6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('ROWBACKGROUNDS', (0, 2), (-1, -2), [colors.HexColor('#fafafa'), colors.white]),
        ('LINEBELOW', (0, -1), (-1, -1), 2, colors.HexColor('#1a237e')),
        ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#1a237e')),
    ]))
    elements.append(table)

    elements.append(Spacer(1, 15))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cccccc')))
    elements.append(Paragraph(
        'This is a computer-generated statement.',
        ParagraphStyle('Footer', parent=style_normal, fontSize=7, textColor=colors.gray, alignment=1)
    ))

    doc.build(elements, onFirstPage=_draw_background, onLaterPages=_draw_background)
    return buf.getvalue()
