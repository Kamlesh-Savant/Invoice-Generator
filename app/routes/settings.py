from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.setting import Setting
from app.models.user import User

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')


@settings_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        action = request.form.get('action', '')

        if action == 'general':
            Setting.set('business_name', request.form.get('business_name', '').strip())
            Setting.set('business_address', request.form.get('business_address', '').strip())
            Setting.set('business_mobile', request.form.get('business_mobile', '').strip())
            Setting.set('business_email', request.form.get('business_email', '').strip())
            Setting.set('business_gst', request.form.get('business_gst', '').strip())
            Setting.set('invoice_prefix', request.form.get('invoice_prefix', 'INV-').strip())
            Setting.set('payment_prefix', request.form.get('payment_prefix', 'PAY-').strip())
            flash('Settings saved successfully.', 'success')

        elif action == 'password':
            current_password = request.form.get('current_password', '')
            new_password = request.form.get('new_password', '')
            confirm_password = request.form.get('confirm_password', '')

            user = User.query.filter_by(is_admin=True).first()
            if not user or not user.check_password(current_password):
                flash('Current password is incorrect.', 'danger')
            elif new_password != confirm_password:
                flash('New passwords do not match.', 'danger')
            elif len(new_password) < 4:
                flash('Password must be at least 4 characters.', 'warning')
            else:
                user.set_password(new_password)
                db.session.commit()
                flash('Password changed successfully.', 'success')

        return redirect(url_for('settings.index'))

    settings = {
        'business_name': Setting.get('business_name', 'My Business'),
        'business_address': Setting.get('business_address', ''),
        'business_mobile': Setting.get('business_mobile', ''),
        'business_email': Setting.get('business_email', ''),
        'business_gst': Setting.get('business_gst', ''),
        'invoice_prefix': Setting.get('invoice_prefix', 'INV-'),
        'payment_prefix': Setting.get('payment_prefix', 'PAY-')
    }

    return render_template('settings/index.html', settings=settings)
