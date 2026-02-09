import logging
from flask import Flask, flash, redirect, url_for
from flask_login import LoginManager, current_user, logout_user
from config import Config
from services.auth_service import get_user_by_id
from services.email_service import init_mail

from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.inventory_routes import inventory_bp
from routes.scan_routes import scan_bp
from routes.warehouse_routes import warehouse_bp
from routes.statistics_routes import statistics_bp
from routes.reports_routes import reports_bp
from routes.request_routes import request_bp


def configure_logging(app):
    """Configure application and tracing loggers"""
    log_level = getattr(logging, str(app.config.get("LOG_LEVEL", "INFO")).upper(), logging.INFO)
    trace_level = getattr(logging, str(app.config.get("TRACE_LEVEL", "WARNING")).upper(), logging.WARNING)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )

    logging.getLogger("dronify.app").setLevel(log_level)
    logging.getLogger("dronify.trace").setLevel(trace_level)
    logging.getLogger("werkzeug").setLevel(logging.WARNING)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    configure_logging(app)

    # Initialize Flask-Mail
    init_mail(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(int(user_id))

    @app.before_request
    def check_user_active():
        if current_user.is_authenticated and not current_user.is_active:
            logout_user()
            flash("Your account has been disabled.", "warning")
            return redirect(url_for("auth.login"))

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(scan_bp)
    app.register_blueprint(warehouse_bp)
    app.register_blueprint(statistics_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(request_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
