"""
Logging Configuration for Housing Management System
تكوين السجلات لنظام إدارة الإسكان
"""

import os
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime

# Create logs directory if it doesn't exist
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

# Log file paths
APP_LOG = os.path.join(LOGS_DIR, 'app.log')
ERROR_LOG = os.path.join(LOGS_DIR, 'error.log')
ACCESS_LOG = os.path.join(LOGS_DIR, 'access.log')
SECURITY_LOG = os.path.join(LOGS_DIR, 'security.log')
AUDIT_LOG = os.path.join(LOGS_DIR, 'audit.log')

# Log format
LOG_FORMAT = '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Security log format (with additional context)
SECURITY_LOG_FORMAT = '[%(asctime)s] SECURITY %(levelname)s: %(message)s'

def setup_logging(app):
    """
    Setup comprehensive logging for Flask application
    إعداد سجلات شاملة لتطبيق Flask
    """
    
    # Determine log level based on environment
    log_level = logging.DEBUG if os.environ.get('FLASK_ENV') == 'development' else logging.INFO
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT
    )
    
    # Remove default handlers
    app.logger.handlers.clear()
    
    # Console Handler (for development)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    console_handler.setFormatter(console_formatter)
    
    # Application Log Handler (rotating)
    app_handler = RotatingFileHandler(
        APP_LOG,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    app_handler.setLevel(logging.INFO)
    app_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    app_handler.setFormatter(app_formatter)
    
    # Error Log Handler (rotating)
    error_handler = RotatingFileHandler(
        ERROR_LOG,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    error_handler.setFormatter(error_formatter)
    
    # Security Log Handler (daily rotation)
    security_handler = TimedRotatingFileHandler(
        SECURITY_LOG,
        when='midnight',
        interval=1,
        backupCount=90  # Keep 90 days of security logs
    )
    security_handler.setLevel(logging.WARNING)
    security_formatter = logging.Formatter(SECURITY_LOG_FORMAT, DATE_FORMAT)
    security_handler.setFormatter(security_formatter)
    
    # Audit Log Handler (daily rotation)
    audit_handler = TimedRotatingFileHandler(
        AUDIT_LOG,
        when='midnight',
        interval=1,
        backupCount=365  # Keep 1 year of audit logs
    )
    audit_handler.setLevel(logging.INFO)
    audit_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    audit_handler.setFormatter(audit_formatter)
    
    # Add handlers to app logger
    if os.environ.get('FLASK_ENV') == 'development':
        app.logger.addHandler(console_handler)
    
    app.logger.addHandler(app_handler)
    app.logger.addHandler(error_handler)
    
    # Set log level
    app.logger.setLevel(log_level)
    
    # Create separate loggers for security and audit
    security_logger = logging.getLogger('security')
    security_logger.addHandler(security_handler)
    security_logger.setLevel(logging.WARNING)
    
    audit_logger = logging.getLogger('audit')
    audit_logger.addHandler(audit_handler)
    audit_logger.setLevel(logging.INFO)
    
    app.logger.info('=' * 80)
    app.logger.info('Housing Management System Starting')
    app.logger.info('نظام إدارة الإسكان يبدأ')
    app.logger.info(f'Environment: {os.environ.get("FLASK_ENV", "production")}')
    app.logger.info(f'Log Level: {logging.getLevelName(log_level)}')
    app.logger.info(f'Logs Directory: {LOGS_DIR}')
    app.logger.info('=' * 80)
    
    return app

def log_security_event(event_type, message, user_id=None, ip_address=None, severity='WARNING'):
    """
    Log security-related events
    تسجيل الأحداث الأمنية
    
    Args:
        event_type: Type of security event (login_failure, access_denied, etc.)
        message: Detailed message
        user_id: User ID if applicable
        ip_address: IP address if applicable
        severity: Log severity (WARNING, ERROR, CRITICAL)
    """
    logger = logging.getLogger('security')
    
    log_message = f"{event_type} | {message}"
    if user_id:
        log_message += f" | User: {user_id}"
    if ip_address:
        log_message += f" | IP: {ip_address}"
    
    if severity == 'CRITICAL':
        logger.critical(log_message)
    elif severity == 'ERROR':
        logger.error(log_message)
    else:
        logger.warning(log_message)

def log_audit_event(action, user_id, details='', ip_address=None):
    """
    Log audit trail events
    تسجيل أحداث سجل التدقيق
    
    Args:
        action: Action performed (create, update, delete, etc.)
        user_id: User who performed the action
        details: Additional details
        ip_address: IP address if applicable
    """
    logger = logging.getLogger('audit')
    
    log_message = f"User {user_id} | Action: {action}"
    if details:
        log_message += f" | Details: {details}"
    if ip_address:
        log_message += f" | IP: {ip_address}"
    
    logger.info(log_message)

# Security event types / أنواع الأحداث الأمنية
SECURITY_EVENTS = {
    'LOGIN_SUCCESS': 'Successful login',
    'LOGIN_FAILURE': 'Failed login attempt',
    'PASSWORD_CHANGE': 'Password changed',
    'PASSWORD_RESET': 'Password reset requested',
    'ACCESS_DENIED': 'Access denied',
    'INVALID_TOKEN': 'Invalid authentication token',
    'SESSION_EXPIRED': 'Session expired',
    'SUSPICIOUS_ACTIVITY': 'Suspicious activity detected',
    'BRUTE_FORCE': 'Possible brute force attack',
    'SQL_INJECTION': 'SQL injection attempt detected',
    'XSS_ATTEMPT': 'XSS attack attempt detected',
    'FILE_UPLOAD_REJECTED': 'Malicious file upload rejected',
}

# Audit action types / أنواع إجراءات التدقيق
AUDIT_ACTIONS = {
    'CREATE': 'Created record',
    'UPDATE': 'Updated record',
    'DELETE': 'Deleted record',
    'VIEW': 'Viewed sensitive data',
    'EXPORT': 'Exported data',
    'IMPORT': 'Imported data',
    'CONFIG_CHANGE': 'Configuration changed',
    'USER_MANAGEMENT': 'User management action',
}

# Example usage in Flask routes:
"""
from config.logging_config import log_security_event, log_audit_event, SECURITY_EVENTS, AUDIT_ACTIONS

# In login endpoint
if login_failed:
    log_security_event(
        'LOGIN_FAILURE',
        f'Failed login for username: {username}',
        ip_address=request.remote_addr,
        severity='WARNING'
    )

# In audit trail
log_audit_event(
    AUDIT_ACTIONS['CREATE'],
    user_id=current_user.id,
    details=f'Created building: {building_name}',
    ip_address=request.remote_addr
)
"""
