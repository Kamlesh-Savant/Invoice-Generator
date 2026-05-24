from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'

    from app.routes.auth import auth_bp
    from app.routes.parties import parties_bp
    from app.routes.invoices import invoices_bp
    from app.routes.payments import payments_bp
    from app.routes.ledger import ledger_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.settings import settings_bp
    from app.routes.exports import exports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(parties_bp)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(ledger_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(exports_bp)

    with app.app_context():
        from app.models.party import Party
        from app.models.invoice import Invoice, InvoiceItem
        from app.models.payment import Payment
        from app.models.setting import Setting
        from app.models.user import User
        db.create_all()

        if not User.query.first():
            admin = User(username='admin', email='admin@example.com')
            admin.set_password('1234')
            db.session.add(admin)

            if not Setting.get('business_name'):
                Setting.set('business_name', 'My Business')
                Setting.set('invoice_prefix', 'INV-')
                Setting.set('payment_prefix', 'PAY-')

            db.session.commit()

    return app
