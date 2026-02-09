# Gmail Email Notifications Setup Guide

## Overview
This guide explains how to configure Gmail SMTP for sending email notifications in the Dronify Inventory Management System.

## Features Implemented
✅ Email notifications to Admin when new requests are created  
✅ Email notifications to Staff when request status changes (APPROVED, REJECTED, COMPLETED)  
✅ HTML and plain text email templates  
✅ Secure Gmail App Password authentication  
✅ Test email functionality

## Prerequisites
- Gmail account with 2-Step Verification enabled
- Python environment with Flask installed

## Step-by-Step Setup

### 1. Enable 2-Step Verification on Your Gmail Account
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Under "Signing in to Google," select **2-Step Verification**
3. Follow the prompts to enable it (if not already enabled)

### 2. Generate Gmail App Password
1. Go to [Google Account](https://myaccount.google.com/)
2. Click on **Security** in the left sidebar
3. Under "Signing in to Google," click **2-Step Verification**
4. Scroll down and click **App passwords**
5. Select **Mail** for the app and **Other** for the device
6. Enter "Dronify" as the device name
7. Click **Generate**
8. **IMPORTANT**: Copy the 16-character password (remove spaces)

### 3. Configure Environment Variables
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your credentials:
   ```env
   # Your Gmail address
   GMAIL_USERNAME=your-email@gmail.com
   
   # The 16-character app password (without spaces)
   GMAIL_APP_PASSWORD=abcdefghijklmnop
   
   # Admin email (who receives notifications)
   ADMIN_EMAIL=admin@example.com
   ```

### 4. Install Dependencies
Make sure all required packages are installed:
```bash
pip install -r requirements.txt
```

This includes:
- `flask-mail` - Email functionality for Flask
- `python-dotenv` - Environment variable management

### 5. Test Email Configuration
Run the test script to verify your setup:
```bash
python test_email.py your-email@example.com
```

You should see:
```
✅ SUCCESS! Test email sent successfully!
Check the inbox of your-email@example.com
```

## Email Notifications Workflow

### When Staff Creates a Request:
1. Staff member submits an inventory request
2. **Admin receives an email** with:
   - Request ID and timestamp
   - Requester name and email
   - Item details (name, type, quantity)
   - Request message
   - Status: PENDING

### When Admin Updates Request Status:
1. Admin approves, rejects, or completes a request
2. **Staff member receives an email** with:
   - Request ID and update timestamp
   - Item details
   - New status (with color coding)
   - Admin note (if provided)

## Email Templates

### Email Content Includes:
- **Professional HTML formatting** with colors and styling
- **Plain text fallback** for email clients without HTML support
- **Status color coding**:
  - 🟢 APPROVED - Green
  - 🔴 REJECTED - Red
  - 🔵 COMPLETED - Blue
  - 🟡 PENDING - Yellow

## Security Best Practices

### ✅ DO:
- Use Gmail App Password (never your regular password)
- Keep `.env` file in `.gitignore`
- Use environment variables for sensitive data
- Enable 2-Step Verification on your Gmail account

### ❌ DON'T:
- Commit `.env` file to version control
- Share your App Password
- Use "Less secure app access" (deprecated by Google)
- Hardcode credentials in code

## Troubleshooting

### Email not sending?
**Check these common issues:**

1. **Invalid credentials**
   - Verify you're using App Password, not regular password
   - Check for typos in GMAIL_USERNAME and GMAIL_APP_PASSWORD
   - Ensure no extra spaces in the app password

2. **2-Step Verification not enabled**
   - App Passwords require 2-Step Verification
   - Enable it in Google Account Security settings

3. **Wrong email format**
   - Ensure GMAIL_USERNAME includes @gmail.com
   - Example: `yourname@gmail.com`

4. **Network/Firewall issues**
   - Check internet connection
   - Ensure port 587 is not blocked
   - Try disabling VPN temporarily

5. **Gmail account restrictions**
   - New accounts may have sending limits
   - Check Gmail's sending limits and quotas

### Testing Tips
```bash
# Test with your own email first
python test_email.py your-email@gmail.com

# Check application logs
python app.py
# Look for "Email sent successfully" messages
```

## Configuration Reference

### SMTP Settings (Configured in config.py)
```python
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
```

### Environment Variables (.env)
```env
GMAIL_USERNAME        # Your Gmail address
GMAIL_APP_PASSWORD    # 16-character app password
ADMIN_EMAIL          # Email to receive admin notifications
```

## Advanced Configuration

### Send Test Email from Python
```python
from app import create_app
from services.email_service import send_test_email

app = create_app()
with app.app_context():
    send_test_email('recipient@example.com')
```

### Customize Email Templates
Email templates are in `services/email_service.py`:
- `send_new_request_notification()` - New request to admin
- `send_request_status_update()` - Status update to staff
- Modify HTML/CSS inline styles as needed

## Additional Resources
- [Gmail App Passwords Guide](https://support.google.com/accounts/answer/185833)
- [Flask-Mail Documentation](https://pythonhosted.org/Flask-Mail/)
- [Google 2-Step Verification](https://www.google.com/landing/2step/)

## Support
If you encounter issues:
1. Run the test script: `python test_email.py`
2. Check console output for error messages
3. Verify .env configuration
4. Review Gmail account security settings

---
**Last Updated**: January 28, 2026
