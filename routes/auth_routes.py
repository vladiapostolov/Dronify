import logging
import re
import dns.resolver
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from models.user import User
from services.auth_service import authenticate, register_user, get_user_by_email, activate_user, is_user_active
from services.email_service import send_verification_email
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

auth_bp = Blueprint("auth", __name__)
logger = logging.getLogger("dronify.app")
trace_logger = logging.getLogger("dronify.trace")


def _serializer():
    return URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"],
        salt=current_app.config.get("VERIFICATION_TOKEN_SALT", "dronify-email-verify")
    )

@auth_bp.route("/")
def home():
    return render_template("welcome.html")

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        
        row = get_user_by_email(email)
        if not row:
            flash("Invalid email or password", "danger")
            logger.warning("Login failed: unknown email", extra={"email": email})
        elif not row.get("is_active", 1):
            flash("Please verify your email to activate your account.", "warning")
            logger.warning("Login blocked: inactive account", extra={"email": email})
            return redirect(url_for("auth.login"))
        elif not check_password_hash(row["password_hash"], password):
            flash("Invalid email or password", "danger")
            trace_logger.info("Login failed: bad password", extra={"email": email})
        else:
            user = User(
                id=row["id"],
                email=row["email"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                role=row["role"],
                is_active=bool(row["is_active"])
            )
            login_user(user)
            logger.info("User logged in", extra={"user_id": user.id, "email": user.email})
            return redirect(url_for("dashboard.dashboard"))
    
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        first_name = request.form["first_name"].strip()
        last_name = request.form["last_name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        confirm_password = request.form.get("confirm_password", "")

        def validation_error(message):
            flash(message, "danger")
            trace_logger.info("Registration validation failed", extra={"email": email, "reason": message})
            return render_template("register.html", form=request.form)

        if not first_name or not last_name:
            return validation_error("First and last name are required.")
        if len(first_name) > 50 or len(last_name) > 50:
            return validation_error("Names must be 50 characters or fewer.")
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            return validation_error("Please enter a valid email address.")
        try:
            domain = email.split("@", 1)[1]
            dns.resolver.resolve(domain, 'MX', lifetime=3.0)
        except Exception:
            return validation_error("Email domain is not reachable. Please use a valid email.")
        if len(password) < 8:
            return validation_error("Password must be at least 8 characters.")
        if password != confirm_password:
            return validation_error("Passwords do not match.")

        if get_user_by_email(email):
            flash("Email already registered", "warning")
            return render_template("register.html", form=request.form)

        user_id = register_user(first_name, last_name, email, password, role="STAFF", is_active=False)
        logger.info("User registered (pending verification)", extra={"email": email, "user_id": user_id})

        # Send verification email
        try:
            token = _serializer().dumps({"user_id": user_id, "email": email})
            verification_link = url_for("auth.verify_email", token=token, _external=True)
            send_verification_email(email, f"{first_name} {last_name}".strip(), verification_link)
            flash("Account created. Check your email to verify your account.", "info")
        except Exception as e:
            logger.exception("Failed to send verification email", extra={"email": email, "user_id": user_id})
            flash("Account created, but we could not send the verification email. Contact support.", "warning")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/verify-email")
def verify_email():
    token = request.args.get("token")
    if not token:
        flash("Invalid verification link.", "danger")
        return redirect(url_for("auth.login"))

    try:
        data = _serializer().loads(
            token,
            max_age=current_app.config.get("VERIFICATION_TOKEN_EXPIRY_SECONDS", 48 * 3600)
        )
        user_id = data.get("user_id")
        email = data.get("email")
    except SignatureExpired:
        flash("Verification link expired. Please request a new one.", "warning")
        return redirect(url_for("auth.login"))
    except (BadSignature, Exception):
        flash("Invalid verification token.", "danger")
        return redirect(url_for("auth.login"))

    if is_user_active(user_id):
        flash("Your account is already verified. Please login.", "info")
        return redirect(url_for("auth.login"))

    try:
        activate_user(user_id)
        logger.info("User verified", extra={"user_id": user_id, "email": email})
        flash("Your email has been verified. You can now log in.", "success")
    except Exception:
        logger.exception("Failed to activate user during verification", extra={"user_id": user_id})
        flash("Could not activate account. Please contact support.", "danger")

    return redirect(url_for("auth.login"))

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
