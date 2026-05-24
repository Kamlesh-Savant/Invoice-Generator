from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app import db
from app.models.party import Party

parties_bp = Blueprint('parties', __name__, url_prefix='/parties')


@parties_bp.route('/')
@login_required
def index():
    search = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 20

    query = Party.query

    if search:
        query = query.filter(
            db.or_(
                Party.party_name.ilike(f'%{search}%'),
                Party.mobile.ilike(f'%{search}%'),
                Party.email.ilike(f'%{search}%')
            )
        )

    query = query.order_by(Party.party_name)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    parties = pagination.items

    party_data = []
    for party in parties:
        party_data.append({
            'id': party.id,
            'party_name': party.party_name,
            'mobile': party.mobile,
            'email': party.email,
            'gst_no': party.gst_no,
            'opening_balance': party.opening_balance,
            'outstanding': party.outstanding(),
            'created_at': party.created_at
        })

    return render_template(
        'parties/index.html',
        parties=party_data,
        pagination=pagination,
        search=search
    )


@parties_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        party_name = request.form.get('party_name', '').strip()
        if not party_name:
            flash('Party name is required.', 'warning')
            return render_template('parties/form.html', party=None, title='Add Party')

        mobile = request.form.get('mobile', '').strip()
        email = request.form.get('email', '').strip()
        gst_no = request.form.get('gst_no', '').strip()
        address = request.form.get('address', '').strip()
        opening_balance = request.form.get('opening_balance', 0)
        notes = request.form.get('notes', '').strip()

        try:
            opening_balance = float(opening_balance) if opening_balance else 0.0
        except ValueError:
            opening_balance = 0.0

        party = Party(
            party_name=party_name,
            mobile=mobile,
            email=email,
            gst_no=gst_no,
            address=address,
            opening_balance=opening_balance,
            notes=notes
        )
        db.session.add(party)
        db.session.commit()
        flash(f'Party "{party_name}" added successfully.', 'success')
        return redirect(url_for('parties.index'))

    return render_template('parties/form.html', party=None, title='Add Party')


@parties_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    party = Party.query.get_or_404(id)

    if request.method == 'POST':
        party_name = request.form.get('party_name', '').strip()
        if not party_name:
            flash('Party name is required.', 'warning')
            return render_template('parties/form.html', party=party, title='Edit Party')

        party.party_name = party_name
        party.mobile = request.form.get('mobile', '').strip()
        party.email = request.form.get('email', '').strip()
        party.gst_no = request.form.get('gst_no', '').strip()
        party.address = request.form.get('address', '').strip()
        party.notes = request.form.get('notes', '').strip()

        opening_balance = request.form.get('opening_balance', 0)
        try:
            party.opening_balance = float(opening_balance) if opening_balance else 0.0
        except ValueError:
            party.opening_balance = 0.0

        db.session.commit()
        flash(f'Party "{party_name}" updated successfully.', 'success')
        return redirect(url_for('parties.index'))

    return render_template('parties/form.html', party=party, title='Edit Party')


@parties_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    party = Party.query.get_or_404(id)
    name = party.party_name
    db.session.delete(party)
    db.session.commit()
    flash(f'Party "{name}" deleted successfully.', 'success')
    return redirect(url_for('parties.index'))


@parties_bp.route('/get/<int:id>')
@login_required
def get(id):
    party = Party.query.get_or_404(id)
    return jsonify({
        'id': party.id,
        'party_name': party.party_name,
        'mobile': party.mobile or '',
        'email': party.email or '',
        'gst_no': party.gst_no or '',
        'address': party.address or '',
        'opening_balance': party.opening_balance,
        'outstanding': party.outstanding(),
        'notes': party.notes or ''
    })


@parties_bp.route('/search')
@login_required
def search():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])

    parties = Party.query.filter(
        db.or_(
            Party.party_name.ilike(f'%{q}%'),
            Party.mobile.ilike(f'%{q}%')
        )
    ).order_by(Party.party_name).limit(20).all()

    results = []
    for party in parties:
        results.append({
            'id': party.id,
            'party_name': party.party_name,
            'mobile': party.mobile or '',
            'outstanding': party.outstanding()
        })

    return jsonify(results)
