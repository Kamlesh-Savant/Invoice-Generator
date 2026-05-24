from app import db
from datetime import datetime


class Party(db.Model):
    __tablename__ = 'parties'

    id = db.Column(db.Integer, primary_key=True)
    party_name = db.Column(db.String(200), nullable=False, index=True)
    mobile = db.Column(db.String(20))
    email = db.Column(db.String(120))
    gst_no = db.Column(db.String(50))
    address = db.Column(db.Text)
    opening_balance = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    invoices = db.relationship('Invoice', backref='party', lazy='dynamic',
                               cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='party', lazy='dynamic',
                               cascade='all, delete-orphan')

    def total_invoices_amount(self):
        result = db.session.query(db.func.coalesce(db.func.sum(Invoice.total_amount), 0))\
            .filter(Invoice.party_id == self.id).scalar()
        return result

    def total_payments_amount(self):
        result = db.session.query(db.func.coalesce(db.func.sum(Payment.amount), 0))\
            .filter(Payment.party_id == self.id).scalar()
        return result

    def outstanding(self):
        return self.opening_balance + self.total_invoices_amount() - self.total_payments_amount()

    def __repr__(self):
        return f'<Party {self.party_name}>'


from app.models.invoice import Invoice
from app.models.payment import Payment
