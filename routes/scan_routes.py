from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from qr.qr_scanner import scan_qr
from services.inventory_service import get_item_details_by_qr, get_item_events, apply_stock_action

scan_bp = Blueprint("scan", __name__)

@scan_bp.route("/scan")
@login_required
def scan():
    qr_code = scan_qr()
    if not qr_code:
        flash("Scan cancelled or camera error", "warning")
        return redirect(url_for("inventory.inventory"))

    item = get_item_details_by_qr(qr_code)
    if not item:
        flash(f"No item found for QR: {qr_code}", "danger")
        return redirect(url_for("inventory.inventory"))

    events = get_item_events(item["id"], limit=15)
    return render_template("item_details.html", item=item, events=events)

@scan_bp.route("/stock/<action>/<int:item_id>", methods=["POST"])
@login_required
def stock_action(action, item_id):
    try:
        qty = int(request.form["quantity"])
        note = request.form.get("note", "").strip() or None
        apply_stock_action(item_id=item_id, user_id=current_user.id, action=action, qty=qty, note=note)
        flash(f"{action} successful", "success")
    except Exception as e:
        flash(f"Operation failed: {e}", "danger")

    # reload item details by item_id -> easiest is to redirect to inventory, or you can add a /item/<id> route later
    return redirect(url_for("inventory.inventory"))
