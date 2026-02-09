import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from services.inventory_service import list_inventory, add_item, ALLOWED_TYPES

inventory_bp = Blueprint("inventory", __name__)
logger = logging.getLogger("dronify.app")
trace_logger = logging.getLogger("dronify.trace")

@inventory_bp.route("/inventory")
@login_required
def inventory():
    items = list_inventory()
    return render_template("inventory.html", items=items, allowed_types=sorted(ALLOWED_TYPES))

@inventory_bp.route("/inventory/add", methods=["POST"])
@login_required
def inventory_add():
    if current_user.role != 'ADMIN':
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for("inventory.inventory"))
    
    name = request.form["name"].strip()
    description = request.form.get("description", "").strip()
    type_ = request.form["type"].strip()
    qr_code = request.form["qr_code"].strip()
    quantity_raw = request.form.get("quantity", "0").strip()

    def invalid(message):
        flash(message, "danger")
        trace_logger.info("Inventory add validation failed", extra={"reason": message, "name": name, "qr_code": qr_code})
        return redirect(url_for("inventory.inventory"))

    if not name or len(name) < 2:
        return invalid("Item name must be at least 2 characters.")
    if len(name) > 120:
        return invalid("Item name is too long (max 120 characters).")

    if type_ not in ALLOWED_TYPES:
        return invalid("Invalid item type selected.")

    try:
        quantity = int(quantity_raw)
    except ValueError:
        return invalid("Quantity must be a whole number.")
    if quantity < 0:
        return invalid("Quantity cannot be negative.")

    if not qr_code or len(qr_code) < 3:
        return invalid("QR code is required and must be at least 3 characters.")
    if len(qr_code) > 100:
        return invalid("QR code is too long (max 100 characters).")

    try:
        add_item(
            name=name,
            description=description,
            type_=type_,
            quantity=quantity,
            qr_code=qr_code
        )
        logger.info("Item added", extra={"name": name, "qr_code": qr_code})
        flash("Item added", "success")
    except Exception as e:
        flash(f"Failed to add item: {e}", "danger")
        logger.exception("Failed to add item", extra={"name": name, "qr_code": qr_code})
    return redirect(url_for("inventory.inventory"))

@inventory_bp.route("/inventory/delete/<int:item_id>", methods=["POST"])
@login_required
def delete_item(item_id):
    if current_user.role != 'ADMIN':
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for("inventory.inventory"))
    
    try:
        from db.connection import db_cursor
        with db_cursor() as (conn, cur):
            # Check if item exists
            cur.execute("SELECT name FROM items WHERE id=%s", (item_id,))
            item = cur.fetchone()
            if not item:
                flash("Item not found.", "danger")
                return redirect(url_for('inventory.inventory'))
            
            # Delete warehouse events first
            cur.execute("DELETE FROM warehouse_events WHERE item_id=%s", (item_id,))
            
            # Delete the item
            cur.execute("DELETE FROM items WHERE id=%s", (item_id,))
            conn.commit()
        
        flash(f"Item '{item['name']}' deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting item: {e}", "danger")
    
    return redirect(url_for('inventory.inventory'))
