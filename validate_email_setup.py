"""
Email Configuration Validation Script

This script validates the email notification setup without sending emails.
Run this to check if configuration is properly set up.
"""

import os
from app import create_app

def validate_config():
    """Validate email configuration"""
    print("=" * 70)
    print("Dronify Email Configuration Validator")
    print("=" * 70)
    
    app = create_app()
    
    with app.app_context():
        # Check Flask-Mail configuration
        print("\n📧 Flask-Mail Configuration:")
        print(f"   MAIL_SERVER: {app.config.get('MAIL_SERVER', 'NOT SET')}")
        print(f"   MAIL_PORT: {app.config.get('MAIL_PORT', 'NOT SET')}")
        print(f"   MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS', 'NOT SET')}")
        print(f"   MAIL_USE_SSL: {app.config.get('MAIL_USE_SSL', 'NOT SET')}")
        
        # Check credentials
        print("\n🔐 Gmail Credentials:")
        username = app.config.get('MAIL_USERNAME')
        password = app.config.get('MAIL_PASSWORD')
        
        if username:
            print(f"   ✅ GMAIL_USERNAME: {username}")
        else:
            print(f"   ❌ GMAIL_USERNAME: NOT CONFIGURED")
        
        if password:
            print(f"   ✅ GMAIL_APP_PASSWORD: {'*' * 16} (configured)")
        else:
            print(f"   ❌ GMAIL_APP_PASSWORD: NOT CONFIGURED")
        
        # Check admin email
        print("\n👤 Admin Configuration:")
        admin_email = app.config.get('ADMIN_EMAIL')
        if admin_email:
            print(f"   ✅ ADMIN_EMAIL: {admin_email}")
        else:
            print(f"   ❌ ADMIN_EMAIL: NOT CONFIGURED")
        
        # Check .env file
        print("\n📄 Environment File:")
        if os.path.exists('.env'):
            print("   ✅ .env file exists")
        else:
            print("   ❌ .env file NOT FOUND")
            print("   💡 Create .env from .env.example")
        
        # Overall status
        print("\n" + "=" * 70)
        if username and password and admin_email:
            print("✅ Configuration Status: COMPLETE")
            print("\n🎯 Next Steps:")
            print("   1. Run: python test_email.py your-email@example.com")
            print("   2. Check your inbox for the test email")
            print("   3. If successful, email notifications are ready!")
        else:
            print("❌ Configuration Status: INCOMPLETE")
            print("\n🔧 Required Actions:")
            if not os.path.exists('.env'):
                print("   1. Copy .env.example to .env")
                print("      Command: cp .env.example .env")
            if not username:
                print("   2. Set GMAIL_USERNAME in .env")
            if not password:
                print("   3. Set GMAIL_APP_PASSWORD in .env")
                print("      See docs/EMAIL_SETUP_GUIDE.md for instructions")
            if not admin_email:
                print("   4. Set ADMIN_EMAIL in .env")
        print("=" * 70)

if __name__ == "__main__":
    try:
        validate_config()
    except Exception as e:
        print(f"\n❌ Error during validation: {str(e)}")
        print("\nMake sure:")
        print("  - All dependencies are installed (pip install -r requirements.txt)")
        print("  - Database is configured correctly")
        print("  - config.py is properly set up")
