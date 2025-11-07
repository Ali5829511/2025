"""
Email notification system for traffic management
نظام الإشعارات عبر البريد الإلكتروني لنظام المرور
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime

# Email configuration from environment variables
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SMTP_USERNAME = os.environ.get('SMTP_USERNAME', '')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
FROM_EMAIL = os.environ.get('FROM_EMAIL', SMTP_USERNAME)
FROM_NAME = os.environ.get('FROM_NAME', 'نظام المرور المتكامل')


def is_configured():
    """Check if email system is configured"""
    return bool(SMTP_USERNAME and SMTP_PASSWORD)


def send_email(to_email, subject, body_html, body_text=None, attachments=None):
    """
    Send email notification
    إرسال إشعار عبر البريد الإلكتروني
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body_html: HTML body content
        body_text: Plain text body (optional, will be generated from HTML if not provided)
        attachments: List of file paths to attach (optional)
    
    Returns:
        dict: {'success': bool, 'message': str, 'error': str (if failed)}
    """
    if not is_configured():
        return {
            'success': False,
            'error': 'Email system is not configured',
            'error_ar': 'نظام البريد الإلكتروني غير مفعل'
        }
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f'{FROM_NAME} <{FROM_EMAIL}>'
        msg['To'] = to_email
        msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
        
        # Add body
        if body_text:
            part1 = MIMEText(body_text, 'plain', 'utf-8')
            msg.attach(part1)
        
        part2 = MIMEText(body_html, 'html', 'utf-8')
        msg.attach(part2)
        
        # Add attachments if any
        if attachments:
            for file_path in attachments:
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {os.path.basename(file_path)}'
                        )
                        msg.attach(part)
        
        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        
        return {
            'success': True,
            'message': 'Email sent successfully',
            'message_ar': 'تم إرسال البريد الإلكتروني بنجاح'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'error_ar': f'خطأ في إرسال البريد الإلكتروني: {str(e)}'
        }


def send_violation_notification(violation_data, recipient_email):
    """Send violation notification email"""
    subject = f'إشعار مخالفة مرورية - {violation_data.get("plate_number", "")}'
    
    body_html = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                direction: rtl;
                text-align: right;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background: #f9fafb;
            }}
            .header {{
                background: linear-gradient(90deg, #0f3d68 0%, #2e8bc0 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            }}
            .content {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            .info-row {{
                padding: 10px;
                border-bottom: 1px solid #e5e7eb;
            }}
            .info-label {{
                font-weight: bold;
                color: #374151;
            }}
            .info-value {{
                color: #6b7280;
            }}
            .footer {{
                margin-top: 20px;
                padding: 15px;
                text-align: center;
                color: #6b7280;
                font-size: 0.9em;
            }}
            .warning {{
                background: #fef3c7;
                border-right: 4px solid #f59e0b;
                padding: 15px;
                margin: 15px 0;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚦 إشعار مخالفة مرورية</h1>
                <p>نظام المرور المتكامل - جامعة الإمام محمد بن سعود الإسلامية</p>
            </div>
            
            <div class="content">
                <div class="warning">
                    <strong>⚠️ تنبيه:</strong> تم تسجيل مخالفة مرورية على مركبتك
                </div>
                
                <div class="info-row">
                    <span class="info-label">رقم اللوحة:</span>
                    <span class="info-value">{violation_data.get('plate_number', 'غير محدد')}</span>
                </div>
                
                <div class="info-row">
                    <span class="info-label">نوع المخالفة:</span>
                    <span class="info-value">{violation_data.get('violation_type', 'غير محدد')}</span>
                </div>
                
                <div class="info-row">
                    <span class="info-label">التاريخ:</span>
                    <span class="info-value">{violation_data.get('violation_date', 'غير محدد')}</span>
                </div>
                
                <div class="info-row">
                    <span class="info-label">الموقع:</span>
                    <span class="info-value">{violation_data.get('location', 'غير محدد')}</span>
                </div>
                
                <div class="info-row">
                    <span class="info-label">مبلغ الغرامة:</span>
                    <span class="info-value" style="color: #ef4444; font-weight: bold;">
                        {violation_data.get('fine_amount', 0)} ريال
                    </span>
                </div>
                
                <p style="margin-top: 20px;">
                    <strong>للاستعلام عن المخالفة والدفع، يرجى زيارة:</strong><br>
                    نظام المرور المتكامل - صفحة الاستعلام
                </p>
            </div>
            
            <div class="footer">
                <p>هذا البريد الإلكتروني آلي، يرجى عدم الرد عليه</p>
                <p>للاستفسارات: traffic@university.edu.sa</p>
                <p>© 2025 جامعة الإمام محمد بن سعود الإسلامية</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(recipient_email, subject, body_html)


def send_accident_notification(accident_data, recipient_email):
    """Send accident notification email"""
    subject = f'إشعار حادث مروري - {accident_data.get("accident_number", "")}'
    
    severity_map = {
        'minor': 'بسيط',
        'moderate': 'متوسط',
        'severe': 'خطير',
        'critical': 'حرج'
    }
    
    body_html = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                direction: rtl;
                text-align: right;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background: #f9fafb;
            }}
            .header {{
                background: linear-gradient(90deg, #ef4444 0%, #f59e0b 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            }}
            .content {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            .info-row {{
                padding: 10px;
                border-bottom: 1px solid #e5e7eb;
            }}
            .info-label {{
                font-weight: bold;
                color: #374151;
            }}
            .info-value {{
                color: #6b7280;
            }}
            .footer {{
                margin-top: 20px;
                padding: 15px;
                text-align: center;
                color: #6b7280;
                font-size: 0.9em;
            }}
            .alert {{
                background: #fee2e2;
                border-right: 4px solid #ef4444;
                padding: 15px;
                margin: 15px 0;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚨 إشعار حادث مروري</h1>
                <p>نظام المرور المتكامل - جامعة الإمام محمد بن سعود الإسلامية</p>
            </div>
            
            <div class="content">
                <div class="alert">
                    <strong>⚠️ تنبيه:</strong> تم تسجيل حادث مروري متعلق بمركبتك
                </div>
                
                <div class="info-row">
                    <span class="info-label">رقم الحادث:</span>
                    <span class="info-value">{accident_data.get('accident_number', 'غير محدد')}</span>
                </div>
                
                <div class="info-row">
                    <span class="info-label">درجة الخطورة:</span>
                    <span class="info-value" style="color: #ef4444; font-weight: bold;">
                        {severity_map.get(accident_data.get('severity', ''), 'غير محدد')}
                    </span>
                </div>
                
                <div class="info-row">
                    <span class="info-label">التاريخ:</span>
                    <span class="info-value">{accident_data.get('accident_date', 'غير محدد')}</span>
                </div>
                
                <div class="info-row">
                    <span class="info-label">الموقع:</span>
                    <span class="info-value">{accident_data.get('location', 'غير محدد')}</span>
                </div>
                
                <div class="info-row">
                    <span class="info-label">عدد المركبات المتورطة:</span>
                    <span class="info-value">{accident_data.get('vehicles_involved', 0)}</span>
                </div>
                
                <p style="margin-top: 20px;">
                    <strong>للاطلاع على تفاصيل الحادث والإجراءات المطلوبة، يرجى التواصل مع:</strong><br>
                    قسم المرور - جامعة الإمام محمد بن سعود الإسلامية
                </p>
            </div>
            
            <div class="footer">
                <p>هذا البريد الإلكتروني آلي، يرجى عدم الرد عليه</p>
                <p>للاستفسارات: traffic@university.edu.sa</p>
                <p>© 2025 جامعة الإمام محمد بن سعود الإسلامية</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(recipient_email, subject, body_html)


def send_immobilization_notification(immobilization_data, recipient_email):
    """Send vehicle immobilization notification"""
    subject = f'إشعار حجز مركبة - {immobilization_data.get("plate_number", "")}'
    
    body_html = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                direction: rtl;
                text-align: right;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background: #f9fafb;
            }}
            .header {{
                background: linear-gradient(90deg, #7c3aed 0%, #db2777 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            }}
            .content {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            .info-row {{
                padding: 10px;
                border-bottom: 1px solid #e5e7eb;
            }}
            .info-label {{
                font-weight: bold;
                color: #374151;
            }}
            .info-value {{
                color: #6b7280;
            }}
            .footer {{
                margin-top: 20px;
                padding: 15px;
                text-align: center;
                color: #6b7280;
                font-size: 0.9em;
            }}
            .critical {{
                background: #fee2e2;
                border-right: 4px solid #dc2626;
                padding: 15px;
                margin: 15px 0;
                border-radius: 5px;
                color: #991b1b;
            }}
            .fees-box {{
                background: #fef3c7;
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚫 إشعار حجز مركبة</h1>
                <p>نظام المرور المتكامل - جامعة الإمام محمد بن سعود الإسلامية</p>
            </div>
            
            <div class="content">
                <div class="critical">
                    <strong>⛔ تنبيه مهم:</strong> تم حجز مركبتك بسبب مخالفات مرورية غير مدفوعة
                </div>
                
                <div class="info-row">
                    <span class="info-label">رقم اللوحة:</span>
                    <span class="info-value">{immobilization_data.get('plate_number', 'غير محدد')}</span>
                </div>
                
                <div class="info-row">
                    <span class="info-label">تاريخ الحجز:</span>
                    <span class="info-value">{immobilization_data.get('immobilized_date', 'غير محدد')}</span>
                </div>
                
                <div class="info-row">
                    <span class="info-label">نوع الحجز:</span>
                    <span class="info-value">
                        {'كبح (Boot)' if immobilization_data.get('immobilization_type') == 'boot' else 'سحب (Tow)'}
                    </span>
                </div>
                
                <div class="info-row">
                    <span class="info-label">السبب:</span>
                    <span class="info-value">{immobilization_data.get('reason', 'غير محدد')}</span>
                </div>
                
                <div class="fees-box">
                    <h3 style="margin-top: 0;">💰 الرسوم والغرامات المستحقة</h3>
                    <div class="info-row">
                        <span class="info-label">الغرامات المستحقة:</span>
                        <span class="info-value">{immobilization_data.get('outstanding_fines', 0)} ريال</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">رسوم السحب:</span>
                        <span class="info-value">{immobilization_data.get('towing_fee', 0)} ريال</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">رسوم التخزين:</span>
                        <span class="info-value">{immobilization_data.get('storage_fee', 0)} ريال</span>
                    </div>
                    <div class="info-row" style="border-bottom: none;">
                        <span class="info-label">الإجمالي:</span>
                        <span class="info-value" style="color: #dc2626; font-weight: bold; font-size: 1.2em;">
                            {immobilization_data.get('total_fees', 0)} ريال
                        </span>
                    </div>
                </div>
                
                <p style="margin-top: 20px;">
                    <strong>لإفراج عن مركبتك:</strong><br>
                    1. قم بدفع جميع الرسوم والغرامات المستحقة<br>
                    2. توجه إلى قسم المرور مع المستندات المطلوبة<br>
                    3. احصل على إذن الإفراج
                </p>
            </div>
            
            <div class="footer">
                <p>هذا البريد الإلكتروني آلي، يرجى عدم الرد عليه</p>
                <p>للاستفسارات: traffic@university.edu.sa</p>
                <p>© 2025 جامعة الإمام محمد بن سعود الإسلامية</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(recipient_email, subject, body_html)


def send_daily_report(report_data, recipient_email):
    """Send daily traffic report"""
    subject = f'تقرير المرور اليومي - {datetime.now().strftime("%Y-%m-%d")}'
    
    body_html = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                direction: rtl;
                text-align: right;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background: #f9fafb;
            }}
            .header {{
                background: linear-gradient(90deg, #059669 0%, #10b981 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
                margin: 20px 0;
            }}
            .stat-card {{
                background: white;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-align: center;
            }}
            .stat-value {{
                font-size: 2em;
                font-weight: bold;
                color: #0f3d68;
            }}
            .stat-label {{
                color: #6b7280;
                margin-top: 5px;
            }}
            .footer {{
                margin-top: 20px;
                padding: 15px;
                text-align: center;
                color: #6b7280;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 تقرير المرور اليومي</h1>
                <p>{datetime.now().strftime("%Y-%m-%d")}</p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{report_data.get('violations_today', 0)}</div>
                    <div class="stat-label">مخالفات اليوم</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{report_data.get('accidents_today', 0)}</div>
                    <div class="stat-label">حوادث اليوم</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{report_data.get('immobilized_today', 0)}</div>
                    <div class="stat-label">سيارات محجوزة</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{report_data.get('revenue_today', 0)}</div>
                    <div class="stat-label">الإيرادات (ريال)</div>
                </div>
            </div>
            
            <div class="footer">
                <p>نظام المرور المتكامل</p>
                <p>© 2025 جامعة الإمام محمد بن سعود الإسلامية</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(recipient_email, subject, body_html)
