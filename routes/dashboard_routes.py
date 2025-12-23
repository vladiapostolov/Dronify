from flask import Blueprint, render_template
from flask_login import login_required, current_user
from services.inventory_service import dashboard_stats

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    stats = dashboard_stats()
    return render_template("dashboard.html", stats=stats, user=current_user)
