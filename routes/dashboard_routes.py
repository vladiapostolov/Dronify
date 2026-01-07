from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from services.inventory_service import dashboard_stats
from db.connection import db_cursor
from werkzeug.security import generate_password_hash

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    stats = dashboard_stats()
    if current_user.role == 'ADMIN':
        with db_cursor() as (_, cur):
            cur.execute("SELECT COUNT(*) as total_users FROM users")
            user_count = cur.fetchone()
            stats = stats or {}
            stats['total_users'] = user_count['total_users'] if user_count else 0
    return render_template("dashboard.html", stats=stats, user=current_user)

@dashboard_bp.route("/users")
@login_required
def manage_users():
    if current_user.role != 'ADMIN':
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for('dashboard.dashboard'))
    
    with db_cursor() as (_, cur):
        cur.execute("SELECT id, first_name, last_name, email, role, is_active, created_at FROM users ORDER BY created_at DESC")
        users = cur.fetchall()
    
    return render_template("users.html", users=users)

@dashboard_bp.route("/users/add", methods=["POST"])
@login_required
def add_user():
    if current_user.role != 'ADMIN':
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for('dashboard.dashboard'))
    
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role', 'STAFF')
    
    if not all([first_name, last_name, email, password]):
        flash("All fields are required.", "danger")
        return redirect(url_for('dashboard.manage_users'))
    
    pwd_hash = generate_password_hash(password)
    
    try:
        with db_cursor() as (conn, cur):
            cur.execute("""
                INSERT INTO users (first_name, last_name, email, password_hash, role)
                VALUES (%s, %s, %s, %s, %s)
            """, (first_name, last_name, email, pwd_hash, role))
            conn.commit()
        flash("User added successfully.", "success")
    except Exception as e:
        flash(f"Error adding user: {str(e)}", "danger")
    
    return redirect(url_for('dashboard.manage_users'))

@dashboard_bp.route("/users/toggle/<int:user_id>", methods=["POST"])
@login_required
def toggle_user_status(user_id):
    if current_user.role != 'ADMIN':
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for('dashboard.dashboard'))
    
    if current_user.id == user_id:
        flash("You cannot disable your own account.", "warning")
        return redirect(url_for('dashboard.manage_users'))
    
    try:
        with db_cursor() as (conn, cur):
            cur.execute("SELECT is_active FROM users WHERE id=%s", (user_id,))
            row = cur.fetchone()
            if not row:
                flash("User not found.", "danger")
                return redirect(url_for('dashboard.manage_users'))
            
            new_status = 0 if row["is_active"] else 1
            cur.execute("UPDATE users SET is_active=%s WHERE id=%s", (new_status, user_id))
            conn.commit()
        
        status_text = "enabled" if new_status else "disabled"
        flash(f"User account {status_text} successfully.", "success")
    except Exception as e:
        flash(f"Error updating user status: {e}", "danger")
    
    return redirect(url_for('dashboard.manage_users'))

@dashboard_bp.route("/users/delete/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    if current_user.role != 'ADMIN':
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for('dashboard.dashboard'))
    
    if current_user.id == user_id:
        flash("You cannot delete your own account.", "warning")
        return redirect(url_for('dashboard.manage_users'))
    
    try:
        with db_cursor() as (conn, cur):
            # Check if user exists
            cur.execute("SELECT first_name, last_name FROM users WHERE id=%s", (user_id,))
            user_row = cur.fetchone()
            if not user_row:
                flash("User not found.", "danger")
                return redirect(url_for('dashboard.manage_users'))
            
            user_name = f"{user_row['first_name']} {user_row['last_name']}"
            
            # Delete warehouse_events first to avoid FK constraint
            cur.execute("DELETE FROM warehouse_events WHERE user_id=%s", (user_id,))
            
            # Delete the user
            cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
            conn.commit()
        
        flash(f"User {user_name} deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting user: {e}", "danger")
    
    return redirect(url_for('dashboard.manage_users'))
