from app import db
from datetime import datetime


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    payment_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    payment_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.id'), nullable=False, index=True)
    payment_mode = db.Column(db.String(50), nullable=False, default='Cash')
    amount = db.Column(db.Float, nullable=False, default=0.0)
    reference_number = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Payment {self.payment_number}>'
