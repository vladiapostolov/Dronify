from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.warehouse import Warehouse
from services.inventory_service import list_inventory, dashboard_stats
from config import Config

warehouse_bp = Blueprint("warehouse", __name__)

@warehouse_bp.route("/warehouse")
@login_required
def warehouse():
    if current_user.role != 'ADMIN':
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for('dashboard.dashboard'))
    
    warehouse = Warehouse.load_by_id(Config.DEFAULT_WAREHOUSE_ID)
    if not warehouse:
        flash("Warehouse not found", "danger")
        return redirect(url_for('dashboard.dashboard'))
    
    # Get items
    items = warehouse.list_items()
    
    # Sorting
    sort_by = request.args.get('sort', 'name')
    reverse = request.args.get('order', 'asc') == 'desc'
    
    if sort_by == 'name':
        items.sort(key=lambda x: x.name, reverse=reverse)
    elif sort_by == 'type':
        items.sort(key=lambda x: x.type, reverse=reverse)
    elif sort_by == 'quantity':
        items.sort(key=lambda x: x.quantity, reverse=reverse)
    
    # Statistics
    stats = dashboard_stats()
    
    return render_template("warehouse.html", warehouse=warehouse, items=items, stats=stats, sort_by=sort_by, order=request.args.get('order', 'asc'))

@warehouse_bp.route("/warehouse/remove/<int:item_id>", methods=["POST"])
@login_required
def remove_item(item_id):
    if current_user.role != 'ADMIN':
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for('warehouse.warehouse'))
    
    try:
        qty = int(request.form["quantity"])
        warehouse = Warehouse.load_by_id(Config.DEFAULT_WAREHOUSE_ID)
        warehouse.remove_item(item_id, current_user.id, qty, "Admin removal")
        flash("Item removed successfully", "success")
    except Exception as e:
        flash(f"Failed to remove item: {e}", "danger")
    
    return redirect(url_for('warehouse.warehouse'))