from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from services.inventory_service import list_inventory, add_item, ALLOWED_TYPES

inventory_bp = Blueprint("inventory", __name__)

@inventory_bp.route("/inventory")
@login_required
def inventory():
    items = list_inventory()
    return render_template("inventory.html", items=items, allowed_types=sorted(ALLOWED_TYPES))

@inventory_bp.route("/inventory/add", methods=["POST"])
@login_required
def inventory_add():
    try:
        add_item(
            name=request.form["name"].strip(),
            description=request.form.get("description", "").strip(),
            type_=request.form["type"],
            quantity=int(request.form["quantity"]),
            qr_code=request.form["qr_code"].strip()
        )
        flash("Item added", "success")
    except Exception as e:
        flash(f"Failed to add item: {e}", "danger")
    return redirect(url_for("inventory.inventory"))
