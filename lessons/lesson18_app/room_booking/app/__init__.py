from flask import Flask
from sqlalchemy.engine import make_url

from app.models import db


def get_safe_database_url(database_url):
    """Return database URL with password hidden for error messages."""
    try:
        return make_url(database_url).render_as_string(hide_password=True)
    except Exception:
        return database_url


def get_readable_connection_error(error):
    if not isinstance(error, UnicodeDecodeError):
        return str(error)

    raw_message = error.object
    if isinstance(raw_message, bytes):
        for encoding in ("utf-8", "cp1250", "latin2", "latin1"):
            try:
                return raw_message.decode(encoding)
            except UnicodeDecodeError:
                continue
        return raw_message.decode("utf-8", errors="replace")

    return str(error)


def create_app(config=None):

    app = Flask(__name__)

    if config is None:
        from config import DevelopmentConfig

        config = DevelopmentConfig

    app.config.from_object(config)

    db.init_app(app)

    from app.routes.bookings import bookings_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.debug import debug_bp
    from app.routes.notifications import notification_bp
    from app.routes.reports import reports_bp

    app.register_blueprint(notification_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(debug_bp)
    app.register_blueprint(reports_bp, url_prefix="/api/reports")

    with app.app_context():
        try:
            db.create_all()
        except Exception as error:
            database_url = app.config.get("SQLALCHEMY_DATABASE_URI", "")
            readable_error = get_readable_connection_error(error)
            safe_database_url = get_safe_database_url(database_url)
            raise RuntimeError(
                "Cannot connect to PostgreSQL.\n"
                f"Database URL: {safe_database_url}\n"
                f"PostgreSQL error: {readable_error}\n"
                "Check DATABASE_URL in room_booking\\.env. The default password "
                "from the lesson may be different from your local PostgreSQL password."
            ) from None

    return app
