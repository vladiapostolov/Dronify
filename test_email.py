"""
Test Email Configuration Script

This script tests the Gmail SMTP configuration for the Dronify application.
Run this after setting up your .env file with Gmail credentials.

Usage:
    python test_email.py your-test-email@example.com
"""

import sys
from app import create_app
from services.email_service import send_test_email

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_email.py <recipient-email>")
        print("Example: python test_email.py admin@example.com")
        sys.exit(1)
    
    recipient = sys.argv[1]
    
    print("=" * 60)
    print("Dronify Email Configuration Test")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        # Display current configuration
        print(f"\nGmail Configuration:")
        print(f"  SMTP Server: {app.config.get('MAIL_SERVER')}")
        print(f"  Port: {app.config.get('MAIL_PORT')}")
        print(f"  TLS: {app.config.get('MAIL_USE_TLS')}")
        print(f"  Username: {app.config.get('MAIL_USERNAME') or 'NOT CONFIGURED'}")
        print(f"  Password: {'*' * 16 if app.config.get('MAIL_PASSWORD') else 'NOT CONFIGURED'}")
        print(f"  Admin Email: {app.config.get('ADMIN_EMAIL') or 'NOT CONFIGURED'}")
        
        if not app.config.get('MAIL_USERNAME') or not app.config.get('MAIL_PASSWORD'):
            print("\n❌ ERROR: Gmail credentials not configured!")
            print("\nPlease follow these steps:")
            print("1. Copy .env.example to .env")
            print("2. Add your Gmail address to GMAIL_USERNAME")
            print("3. Generate an App Password from your Google Account:")
            print("   - Go to https://myaccount.google.com/")
            print("   - Security → 2-Step Verification → App passwords")
            print("   - Generate a new app password for 'Mail'")
            print("4. Add the 16-character app password to GMAIL_APP_PASSWORD")
            sys.exit(1)
        
        print(f"\nSending test email to: {recipient}")
        print("Please wait...")
        
        success = send_test_email(recipient)
        
        if success:
            print("\n✅ SUCCESS! Test email sent successfully!")
            print(f"Check the inbox of {recipient}")
        else:
            print("\n❌ FAILED! Could not send test email.")
            print("\nTroubleshooting tips:")
            print("1. Verify your Gmail App Password (not your regular password)")
            print("2. Ensure 2-Step Verification is enabled on your Google Account")
            print("3. Check that 'Less secure app access' is NOT required (use App Password)")
            print("4. Verify the recipient email address is correct")
            print("5. Check your internet connection")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
