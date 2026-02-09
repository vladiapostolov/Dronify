from flask import current_app, render_template_string
from flask_mail import Mail, Message
from datetime import datetime
import logging

mail = Mail()
logger = logging.getLogger("dronify.app")

def init_mail(app):
    """Initialize Flask-Mail with the Flask app"""
    mail.init_app(app)

def send_email(to, subject, body, html=None):
    """
    Send an email using Gmail SMTP
    
    Args:
        to: Recipient email address or list of addresses
        subject: Email subject
        body: Plain text email body
        html: HTML email body (optional)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        if not current_app.config.get('MAIL_USERNAME'):
            print("WARNING: Gmail credentials not configured. Email not sent.")
            return False

        msg = Message(
            subject=subject,
            recipients=[to] if isinstance(to, str) else to,
            body=body,
            html=html
        )

        mail.send(msg)
        logger.info("Email sent", extra={"to": to, "subject": subject})
        return True
    except Exception as e:
        logger.exception("Error sending email", extra={"to": to, "subject": subject})
        return False


def send_verification_email(to_email: str, name: str, verification_link: str):
        """Send account verification email"""
        subject = "Verify your Dronify account"
        safe_name = name or "there"

        body = f"""
Hi {safe_name},

Thanks for registering with Dronify. Please verify your email address to activate your account.

Verification link:
{verification_link}

This link will expire in 48 hours. If you did not sign up, please ignore this email.

— Dronify Team
"""

        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #111827;">
            <div style="max-width:600px;margin:0 auto;padding:24px;background:#ffffff;border:1px solid #e5e7eb;border-radius:12px;">
                <h2 style="color:#2563eb; margin-top:0;">Verify your Dronify account</h2>
                <p>Hi {safe_name},</p>
                <p>Thanks for registering with Dronify. Please verify your email address to activate your account.</p>
                <p style="text-align:center;margin:28px 0;">
                    <a href="{verification_link}" style="display:inline-block;padding:12px 20px;background:#2563eb;color:#fff;text-decoration:none;border-radius:8px;font-weight:600;">Verify Email</a>
                </p>
                <p>If the button does not work, copy and paste this link:</p>
                <code style="display:block;word-break:break-all;padding:10px;background:#f3f4f6;border-radius:8px;">{verification_link}</code>
                <p style="color:#6b7280;">This link will expire in 48 hours. If you did not sign up, please ignore this email.</p>
                <p style="margin-top:32px;color:#6b7280;">— Dronify Team</p>
            </div>
        </body>
        </html>
        """

        return send_email(to_email, subject, body, html)

def send_new_request_notification(request_data, user_data, item_data):
    """
    Send notification to admin when a new request is created
    
    Args:
        request_data: Dictionary with request information
        user_data: Dictionary with user information
        item_data: Dictionary with item information
    """
    admin_email = current_app.config.get('ADMIN_EMAIL')
    
    if not admin_email:
        print("WARNING: Admin email not configured")
        return False
    
    subject = f"New Inventory Request - {item_data.get('name')}"
    
    body = f"""
New Inventory Request Received

Request ID: {request_data.get('id')}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Requested By: {user_data.get('name')}
Email: {user_data.get('email')}

Item Details:
- Name: {item_data.get('name')}
- Type: {item_data.get('type')}
- Quantity Requested: {request_data.get('quantity')}

Message: {request_data.get('message') or 'No message provided'}

Status: PENDING

Please review this request in the Dronify admin dashboard.
    """
    
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2563eb; border-bottom: 2px solid #2563eb; padding-bottom: 10px;">
                New Inventory Request
            </h2>
            
            <div style="background-color: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Request ID:</strong> #{request_data.get('id')}</p>
                <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <h3 style="color: #1f2937;">Requester Information</h3>
            <ul style="list-style: none; padding: 0;">
                <li><strong>Name:</strong> {user_data.get('name')}</li>
                <li><strong>Email:</strong> {user_data.get('email')}</li>
            </ul>
            
            <h3 style="color: #1f2937;">Item Details</h3>
            <ul style="list-style: none; padding: 0;">
                <li><strong>Item Name:</strong> {item_data.get('name')}</li>
                <li><strong>Type:</strong> {item_data.get('type')}</li>
                <li><strong>Quantity Requested:</strong> {request_data.get('quantity')}</li>
            </ul>
            
            <div style="background-color: #fef3c7; padding: 15px; border-left: 4px solid #f59e0b; margin: 20px 0;">
                <strong>Message:</strong><br>
                {request_data.get('message') or '<em>No message provided</em>'}
            </div>
            
            <div style="background-color: #dbeafe; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <strong>Status:</strong> <span style="color: #f59e0b;">PENDING</span>
            </div>
            
            <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
                Please review this request in your Dronify admin dashboard.
            </p>
        </div>
    </body>
    </html>
    """
    
    return send_email(admin_email, subject, body, html)

def send_request_status_update(request_data, user_data, item_data, new_status, admin_note=None):
    """
    Send notification to user when their request status is updated
    
    Args:
        request_data: Dictionary with request information
        user_data: Dictionary with user information
        item_data: Dictionary with item information
        new_status: New status of the request (APPROVED, REJECTED, COMPLETED)
        admin_note: Optional note from admin
    """
    user_email = user_data.get('email')
    
    if not user_email:
        print("WARNING: User email not available")
        return False
    
    status_colors = {
        'APPROVED': '#10b981',
        'REJECTED': '#ef4444',
        'COMPLETED': '#3b82f6',
        'PENDING': '#f59e0b'
    }
    
    status_color = status_colors.get(new_status, '#6b7280')
    
    subject = f"Request Update - {item_data.get('name')} - {new_status}"
    
    body = f"""
Your Inventory Request Has Been Updated

Request ID: {request_data.get('id')}
Date Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Item Details:
- Name: {item_data.get('name')}
- Type: {item_data.get('type')}
- Quantity Requested: {request_data.get('quantity')}

New Status: {new_status}

{f'Admin Note: {admin_note}' if admin_note else ''}

Thank you for using Dronify Inventory Management System.
    """
    
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2563eb; border-bottom: 2px solid #2563eb; padding-bottom: 10px;">
                Request Status Update
            </h2>
            
            <div style="background-color: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Request ID:</strong> #{request_data.get('id')}</p>
                <p><strong>Date Updated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <h3 style="color: #1f2937;">Item Details</h3>
            <ul style="list-style: none; padding: 0;">
                <li><strong>Item Name:</strong> {item_data.get('name')}</li>
                <li><strong>Type:</strong> {item_data.get('type')}</li>
                <li><strong>Quantity Requested:</strong> {request_data.get('quantity')}</li>
            </ul>
            
            <div style="background-color: {status_color}22; padding: 15px; border-left: 4px solid {status_color}; margin: 20px 0;">
                <strong>New Status:</strong> <span style="color: {status_color}; font-size: 18px;">{new_status}</span>
            </div>
            
            {f'''
            <div style="background-color: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <strong>Admin Note:</strong><br>
                {admin_note}
            </div>
            ''' if admin_note else ''}
            
            <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb; color: #6b7280;">
                Thank you for using Dronify Inventory Management System.
            </p>
        </div>
    </body>
    </html>
    """
    
    return send_email(user_email, subject, body, html)

def send_test_email(to_email):
    """
    Send a test email to verify Gmail configuration
    
    Args:
        to_email: Email address to send test email to
    
    Returns:
        bool: True if successful, False otherwise
    """
    subject = "Dronify - Test Email"
    body = """
This is a test email from Dronify Inventory Management System.

If you received this email, your Gmail SMTP configuration is working correctly!

Configuration Details:
- SMTP Server: smtp.gmail.com
- Port: 587
- TLS: Enabled

Sent at: {}
    """.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    html = """
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #10b981; border-bottom: 2px solid #10b981; padding-bottom: 10px;">
                ✓ Dronify Test Email
            </h2>
            
            <div style="background-color: #d1fae5; padding: 20px; border-radius: 5px; margin: 20px 0;">
                <p style="font-size: 16px; margin: 0;">
                    <strong>Success!</strong> Your Gmail SMTP configuration is working correctly.
                </p>
            </div>
            
            <h3 style="color: #1f2937;">Configuration Details</h3>
            <ul>
                <li><strong>SMTP Server:</strong> smtp.gmail.com</li>
                <li><strong>Port:</strong> 587</li>
                <li><strong>TLS:</strong> Enabled</li>
            </ul>
            
            <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb; color: #6b7280;">
                <strong>Sent at:</strong> {}
            </p>
        </div>
    </body>
    </html>
    """.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    return send_email(to_email, subject, body, html)
