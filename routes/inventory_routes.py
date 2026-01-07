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
    if current_user.role != 'ADMIN':
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for("inventory.inventory"))
    
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
