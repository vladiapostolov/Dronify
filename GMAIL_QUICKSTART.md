# Quick Start: Gmail Email Notifications

## 🚀 Quick Setup (5 minutes)

### 1. Generate Gmail App Password
```
1. Visit: https://myaccount.google.com/security
2. Enable 2-Step Verification (if not enabled)
3. Go to App Passwords
4. Create password for "Mail" → "Dronify"
5. Copy the 16-character password
```

### 2. Configure Environment
```bash
# Copy template
cp .env.example .env

# Edit .env and add:
GMAIL_USERNAME=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-char-password
ADMIN_EMAIL=admin@example.com
```

### 3. Validate Setup
```bash
python validate_email_setup.py
```

### 4. Test Email
```bash
python test_email.py your-email@example.com
```

## 📧 Email Notifications

### Admin Receives:
- ✉️ New request created by staff
- 📋 Request details (item, quantity, message)
- 🔔 Real-time notification via email

### Staff Receives:
- ✉️ Request status updates
- ✅ APPROVED notifications
- ❌ REJECTED notifications  
- ✔️ COMPLETED notifications
- 📝 Admin notes

## 🔧 Troubleshooting

### Not receiving emails?
```bash
# Check configuration
python validate_email_setup.py

# Common fixes:
1. Use App Password (not regular password)
2. Enable 2-Step Verification
3. Check .env file exists
4. Verify no typos in credentials
```

## 📚 Full Documentation
See [docs/EMAIL_SETUP_GUIDE.md](docs/EMAIL_SETUP_GUIDE.md) for complete setup instructions.

## 🎯 Features
- ✅ Gmail SMTP integration
- ✅ Professional HTML email templates
- ✅ Automatic notifications
- ✅ Secure App Password authentication
- ✅ Admin and staff notifications
- ✅ Status color coding
- ✅ Test email functionality
