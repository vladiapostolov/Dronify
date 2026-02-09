import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "vladi2004")
    DB_NAME = os.getenv("DB_NAME", "Dronify")

    DEFAULT_WAREHOUSE_ID = 1

    # Logging configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    TRACE_LEVEL = os.getenv("TRACE_LEVEL", "WARNING")

    # Email verification
    VERIFICATION_TOKEN_SALT = os.getenv("VERIFICATION_TOKEN_SALT", "dronify-email-verify")
    VERIFICATION_TOKEN_EXPIRY_SECONDS = int(os.getenv("VERIFICATION_TOKEN_EXPIRY_SECONDS", 48 * 3600))

    # Gmail SMTP Configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('GMAIL_USERNAME')  # Your Gmail address
    MAIL_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')  # Gmail App Password
    MAIL_DEFAULT_SENDER = os.getenv('GMAIL_USERNAME')
    
    # Admin Email Configuration
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', os.getenv('GMAIL_USERNAME'))

