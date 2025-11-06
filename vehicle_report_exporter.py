"""
Vehicle Report Exporter Module
نظام تصدير تقارير السيارات والمخالفات

This module provides comprehensive export functionality for vehicle reports:
- Single vehicle reports with all violations
- All vehicles report with complete data
- Export to PDF, Excel, and HTML formats
- Professional formatting with thumbnails and details
"""

import os
from datetime import datetime
from typing import List, Dict, Optional
import database
from io import BytesIO
from PIL import Image


def get_vehicle_with_violations(vehicle_id: int) -> Optional[Dict]:
    """
    Get vehicle details with all associated violations
    الحصول على تفاصيل السيارة مع جميع المخالفات المرتبطة
    
    Args:
        vehicle_id: Vehicle ID
    
    Returns:
        Dict with vehicle and violations data
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        # Get vehicle details
        cursor.execute('''
            SELECT 
                v.*,
                r.name as owner_name,
                r.national_id as owner_national_id,
                r.phone as owner_phone,
                r.email as owner_email,
                r.department,
                r.job_title,
                r.unit_number,
                b.name as building_name,
                b.building_number
            FROM vehicles v
            LEFT JOIN residents r ON v.owner_id = r.id
            LEFT JOIN buildings b ON r.building_id = b.id
            WHERE v.id = ?
        ''', (vehicle_id,))
        
        vehicle_row = cursor.fetchone()
        if not vehicle_row:
            conn.close()
            return None
        
        vehicle = dict(vehicle_row)
        
        # Get violations for this vehicle
        cursor.execute('''
            SELECT 
                tv.*,
                u.name as reported_by_name
            FROM traffic_violations tv
            LEFT JOIN users u ON tv.reported_by = u.id
            WHERE tv.vehicle_id = ?
            ORDER BY tv.violation_date DESC
        ''', (vehicle_id,))
        
        violations = [dict(row) for row in cursor.fetchall()]
        vehicle['violations'] = violations
        vehicle['violation_count'] = len(violations)
        
        # Get car images if available
        cursor.execute('''
            SELECT ci.*, ca.plate_confidence, ca.vehicle_type as detected_type, ca.vehicle_color as detected_color
            FROM car_images ci
            LEFT JOIN car_analysis ca ON ci.id = ca.car_image_id
            WHERE ca.vehicle_id = ?
            ORDER BY ci.uploaded_at DESC
            LIMIT 5
        ''', (vehicle_id,))
        
        images = [dict(row) for row in cursor.fetchall()]
        vehicle['images'] = images
        
        conn.close()
        return vehicle
        
    except Exception as e:
        print(f"Error getting vehicle with violations: {str(e)}")
        return None


def get_all_vehicles_with_violations() -> List[Dict]:
    """
    Get all vehicles with their violations
    الحصول على جميع السيارات مع مخالفاتها
    
    Returns:
        List of vehicles with violations
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        # Get all active vehicles
        cursor.execute('''
            SELECT 
                v.*,
                r.name as owner_name,
                r.national_id as owner_national_id,
                r.phone as owner_phone,
                r.email as owner_email,
                r.department,
                r.job_title,
                r.unit_number,
                b.name as building_name,
                b.building_number,
                COUNT(tv.id) as violation_count
            FROM vehicles v
            LEFT JOIN residents r ON v.owner_id = r.id
            LEFT JOIN buildings b ON r.building_id = b.id
            LEFT JOIN traffic_violations tv ON v.id = tv.vehicle_id
            WHERE v.is_active = 1
            GROUP BY v.id
            ORDER BY v.plate_number
        ''')
        
        vehicles = []
        for row in cursor.fetchall():
            vehicle = dict(row)
            
            # Get violations for each vehicle
            cursor.execute('''
                SELECT 
                    tv.*,
                    u.name as reported_by_name
                FROM traffic_violations tv
                LEFT JOIN users u ON tv.reported_by = u.id
                WHERE tv.vehicle_id = ?
                ORDER BY tv.violation_date DESC
            ''', (vehicle['id'],))
            
            vehicle['violations'] = [dict(v) for v in cursor.fetchall()]
            
            # Get thumbnail if available
            cursor.execute('''
                SELECT ci.thumbnail_path
                FROM car_images ci
                LEFT JOIN car_analysis ca ON ci.id = ca.car_image_id
                WHERE ca.vehicle_id = ?
                ORDER BY ci.uploaded_at DESC
                LIMIT 1
            ''', (vehicle['id'],))
            
            thumbnail_row = cursor.fetchone()
            vehicle['thumbnail_path'] = thumbnail_row[0] if thumbnail_row else None
            
            vehicles.append(vehicle)
        
        conn.close()
        return vehicles
        
    except Exception as e:
        print(f"Error getting all vehicles: {str(e)}")
        return []


def export_vehicle_to_excel(vehicle: Dict, output_path: str) -> bool:
    """
    Export single vehicle report to Excel
    تصدير تقرير السيارة إلى Excel
    
    Args:
        vehicle: Vehicle data with violations
        output_path: Output file path
    
    Returns:
        True if successful
    """
    try:
        import xlsxwriter
        
        workbook = xlsxwriter.Workbook(output_path)
        worksheet = workbook.add_worksheet('تقرير السيارة')
        
        # Set RTL
        worksheet.right_to_left()
        
        # Define formats
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 20,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#0f3d68',
            'font_color': 'white',
            'border': 1
        })
        
        header_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'right',
            'valign': 'vcenter',
            'fg_color': '#2e8bc0',
            'font_color': 'white',
            'border': 1
        })
        
        label_format = workbook.add_format({
            'bold': True,
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'fg_color': '#e8f4f8'
        })
        
        value_format = workbook.add_format({
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'text_wrap': True
        })
        
        violation_header_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#ff6b6b',
            'font_color': 'white',
            'border': 1
        })
        
        violation_cell_format = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'text_wrap': True
        })
        
        # Set column widths
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 30)
        worksheet.set_column('C:C', 25)
        worksheet.set_column('D:D', 30)
        
        # Row counter
        row = 0
        
        # Title and date
        current_date = datetime.now().strftime('%Y/%m/%d %H:%M')
        worksheet.merge_range(row, 0, row, 3, f'تقرير السيارة - {current_date}', title_format)
        worksheet.set_row(row, 35)
        row += 2
        
        # Vehicle Information Section
        worksheet.merge_range(row, 0, row, 3, 'بيانات السيارة', header_format)
        worksheet.set_row(row, 25)
        row += 1
        
        # Vehicle details
        vehicle_data = [
            ('رقم اللوحة', vehicle.get('plate_number', 'غير محدد')),
            ('نوع السيارة', vehicle.get('vehicle_type', 'غير محدد')),
            ('الماركة', vehicle.get('make', 'غير محدد')),
            ('الموديل', vehicle.get('model', 'غير محدد')),
            ('السنة', vehicle.get('year', 'غير محدد')),
            ('اللون', vehicle.get('color', 'غير محدد')),
            ('رقم الملصق', vehicle.get('sticker_number', 'غير محدد')),
            ('تاريخ إصدار الملصق', vehicle.get('sticker_issued_date', 'غير محدد')),
            ('تاريخ انتهاء الملصق', vehicle.get('sticker_expiry_date', 'غير محدد')),
        ]
        
        for label, value in vehicle_data:
            worksheet.write(row, 0, label, label_format)
            worksheet.write(row, 1, str(value), value_format)
            row += 1
        
        row += 1
        
        # Owner Information Section
        worksheet.merge_range(row, 0, row, 3, 'بيانات المالك', header_format)
        worksheet.set_row(row, 25)
        row += 1
        
        owner_data = [
            ('اسم المالك', vehicle.get('owner_name', 'غير محدد')),
            ('الرقم الوطني', vehicle.get('owner_national_id', 'غير محدد')),
            ('الهاتف', vehicle.get('owner_phone', 'غير محدد')),
            ('البريد الإلكتروني', vehicle.get('owner_email', 'غير محدد')),
            ('القسم', vehicle.get('department', 'غير محدد')),
            ('المسمى الوظيفي', vehicle.get('job_title', 'غير محدد')),
            ('رقم الوحدة', vehicle.get('unit_number', 'غير محدد')),
            ('اسم المبنى', vehicle.get('building_name', 'غير محدد')),
        ]
        
        for label, value in owner_data:
            worksheet.write(row, 0, label, label_format)
            worksheet.write(row, 1, str(value), value_format)
            row += 1
        
        row += 2
        
        # Violations Section
        violations = vehicle.get('violations', [])
        worksheet.merge_range(row, 0, row, 3, f'المخالفات المرورية (العدد: {len(violations)})', header_format)
        worksheet.set_row(row, 25)
        row += 1
        
        if violations:
            # Violation headers
            violation_headers = ['#', 'نوع المخالفة', 'التاريخ', 'الموقع', 'الوصف', 'الغرامة', 'الحالة', 'المُبلِّغ']
            for col, header in enumerate(violation_headers):
                worksheet.write(row, col % 4, header, violation_header_format)
                if col >= 4:
                    worksheet.write(row + 1, col - 4, header, violation_header_format)
            row += 2
            
            # Violation data
            for idx, violation in enumerate(violations, 1):
                violation_date = violation.get('violation_date', '')
                if violation_date:
                    try:
                        dt = datetime.fromisoformat(violation_date)
                        violation_date = dt.strftime('%Y/%m/%d %H:%M')
                    except:
                        pass
                
                worksheet.write(row, 0, idx, violation_cell_format)
                worksheet.write(row, 1, violation.get('violation_type', ''), violation_cell_format)
                worksheet.write(row, 2, violation_date, violation_cell_format)
                worksheet.write(row, 3, violation.get('location', ''), violation_cell_format)
                row += 1
                
                worksheet.write(row, 0, 'الوصف:', label_format)
                worksheet.write(row, 1, violation.get('description', ''), violation_cell_format)
                worksheet.write(row, 2, f"{violation.get('fine_amount', 0)} ريال", violation_cell_format)
                worksheet.write(row, 3, violation.get('status', ''), violation_cell_format)
                row += 1
                
                worksheet.write(row, 0, 'المُبلِّغ:', label_format)
                worksheet.write(row, 1, violation.get('reported_by_name', 'غير محدد'), violation_cell_format)
                row += 2
        else:
            worksheet.merge_range(row, 0, row, 3, 'لا توجد مخالفات مسجلة لهذه السيارة', value_format)
            row += 1
        
        workbook.close()
        return True
        
    except Exception as e:
        print(f"Error exporting vehicle to Excel: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def export_all_vehicles_to_excel(vehicles: List[Dict], output_path: str) -> bool:
    """
    Export all vehicles report to Excel
    تصدير تقرير جميع السيارات إلى Excel
    
    Args:
        vehicles: List of vehicles with violations
        output_path: Output file path
    
    Returns:
        True if successful
    """
    try:
        import xlsxwriter
        
        workbook = xlsxwriter.Workbook(output_path)
        worksheet = workbook.add_worksheet('جميع السيارات')
        
        worksheet.right_to_left()
        
        # Define formats
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 18,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#0f3d68',
            'font_color': 'white',
            'border': 1
        })
        
        header_format = workbook.add_format({
            'bold': True,
            'font_size': 11,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#2e8bc0',
            'font_color': 'white',
            'border': 1,
            'text_wrap': True
        })
        
        cell_format = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'text_wrap': True
        })
        
        # Set column widths
        worksheet.set_column('A:A', 5)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 12)
        worksheet.set_column('E:E', 12)
        worksheet.set_column('F:F', 10)
        worksheet.set_column('G:G', 12)
        worksheet.set_column('H:H', 20)
        worksheet.set_column('I:I', 15)
        worksheet.set_column('J:J', 12)
        
        # Title
        current_date = datetime.now().strftime('%Y/%m/%d %H:%M')
        worksheet.merge_range('A1:J1', f'تقرير جميع السيارات - {current_date}', title_format)
        worksheet.set_row(0, 30)
        
        # Headers
        headers = ['#', 'رقم اللوحة', 'نوع السيارة', 'الماركة', 'الموديل', 'اللون', 'رقم الملصق', 
                   'اسم المالك', 'رقم الوحدة', 'عدد المخالفات']
        
        for col, header in enumerate(headers):
            worksheet.write(1, col, header, header_format)
        worksheet.set_row(1, 25)
        
        # Data
        for idx, vehicle in enumerate(vehicles, 1):
            row = idx + 1
            worksheet.set_row(row, 20)
            
            worksheet.write(row, 0, idx, cell_format)
            worksheet.write(row, 1, vehicle.get('plate_number', ''), cell_format)
            worksheet.write(row, 2, vehicle.get('vehicle_type', ''), cell_format)
            worksheet.write(row, 3, vehicle.get('make', ''), cell_format)
            worksheet.write(row, 4, vehicle.get('model', ''), cell_format)
            worksheet.write(row, 5, vehicle.get('color', ''), cell_format)
            worksheet.write(row, 6, vehicle.get('sticker_number', ''), cell_format)
            worksheet.write(row, 7, vehicle.get('owner_name', ''), cell_format)
            worksheet.write(row, 8, vehicle.get('unit_number', ''), cell_format)
            worksheet.write(row, 9, vehicle.get('violation_count', 0), cell_format)
        
        workbook.close()
        return True
        
    except Exception as e:
        print(f"Error exporting all vehicles to Excel: {str(e)}")
        return False


def export_vehicle_to_pdf(vehicle: Dict, output_path: str) -> bool:
    """
    Export single vehicle report to PDF
    تصدير تقرير السيارة إلى PDF
    
    Args:
        vehicle: Vehicle data with violations
        output_path: Output file path
    
    Returns:
        True if successful
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_RIGHT
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#0f3d68'),
            alignment=TA_CENTER,
            spaceAfter=30
        )
        
        current_date = datetime.now().strftime('%Y/%m/%d %H:%M')
        title = Paragraph(f'Vehicle Report - تقرير السيارة<br/>{current_date}', title_style)
        elements.append(title)
        
        # Vehicle Information
        section_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2e8bc0'),
            alignment=TA_RIGHT,
            spaceAfter=10
        )
        
        elements.append(Paragraph('Vehicle Information - بيانات السيارة', section_style))
        
        vehicle_data = [
            ['Plate Number\nرقم اللوحة', vehicle.get('plate_number', 'N/A')],
            ['Type\nنوع السيارة', vehicle.get('vehicle_type', 'N/A')],
            ['Make\nالماركة', vehicle.get('make', 'N/A')],
            ['Model\nالموديل', vehicle.get('model', 'N/A')],
            ['Year\nالسنة', str(vehicle.get('year', 'N/A'))],
            ['Color\nاللون', vehicle.get('color', 'N/A')],
            ['Sticker Number\nرقم الملصق', vehicle.get('sticker_number', 'N/A')],
        ]
        
        vehicle_table = Table(vehicle_data, colWidths=[2.5*inch, 3.5*inch])
        vehicle_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ]))
        
        elements.append(vehicle_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Owner Information
        elements.append(Paragraph('Owner Information - بيانات المالك', section_style))
        
        owner_data = [
            ['Owner Name\nاسم المالك', vehicle.get('owner_name', 'N/A')],
            ['National ID\nالرقم الوطني', vehicle.get('owner_national_id', 'N/A')],
            ['Phone\nالهاتف', vehicle.get('owner_phone', 'N/A')],
            ['Department\nالقسم', vehicle.get('department', 'N/A')],
            ['Job Title\nالمسمى الوظيفي', vehicle.get('job_title', 'N/A')],
            ['Unit Number\nرقم الوحدة', vehicle.get('unit_number', 'N/A')],
        ]
        
        owner_table = Table(owner_data, colWidths=[2.5*inch, 3.5*inch])
        owner_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ]))
        
        elements.append(owner_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Violations
        violations = vehicle.get('violations', [])
        violation_title = f'Traffic Violations - المخالفات المرورية ({len(violations)})'
        elements.append(Paragraph(violation_title, section_style))
        
        if violations:
            for idx, violation in enumerate(violations, 1):
                violation_date = violation.get('violation_date', '')
                if violation_date:
                    try:
                        dt = datetime.fromisoformat(violation_date)
                        violation_date = dt.strftime('%Y/%m/%d %H:%M')
                    except:
                        pass
                
                violation_data = [
                    [f'Violation #{idx}', ''],
                    ['Type\nالنوع', violation.get('violation_type', 'N/A')],
                    ['Date\nالتاريخ', violation_date],
                    ['Location\nالموقع', violation.get('location', 'N/A')],
                    ['Description\nالوصف', violation.get('description', 'N/A')],
                    ['Fine\nالغرامة', f"{violation.get('fine_amount', 0)} SAR"],
                    ['Status\nالحالة', violation.get('status', 'N/A')],
                ]
                
                violation_table = Table(violation_data, colWidths=[2.5*inch, 3.5*inch])
                violation_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff6b6b')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#ffe8e8')),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('ALIGN', (0, 1), (0, -1), 'RIGHT'),
                    ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                
                elements.append(violation_table)
                elements.append(Spacer(1, 0.2*inch))
        else:
            no_violations = Paragraph('No violations recorded - لا توجد مخالفات مسجلة', styles['Normal'])
            elements.append(no_violations)
        
        doc.build(elements)
        return True
        
    except Exception as e:
        print(f"Error exporting vehicle to PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def export_vehicle_to_html(vehicle: Dict, output_path: str) -> bool:
    """
    Export single vehicle report to HTML
    تصدير تقرير السيارة إلى HTML
    
    Args:
        vehicle: Vehicle data with violations
        output_path: Output file path
    
    Returns:
        True if successful
    """
    try:
        from jinja2 import Template
        
        template_str = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تقرير السيارة - {{ vehicle.plate_number }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(90deg, #0f3d68 60%, #2e8bc0 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .content {
            padding: 30px;
        }
        
        .section {
            margin-bottom: 30px;
        }
        
        .section-title {
            background: #2e8bc0;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            font-size: 1.3em;
            margin-bottom: 15px;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }
        
        .info-item {
            display: flex;
            flex-direction: column;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 5px;
            border-right: 3px solid #2e8bc0;
        }
        
        .info-label {
            font-weight: bold;
            color: #0f3d68;
            margin-bottom: 5px;
            font-size: 0.9em;
        }
        
        .info-value {
            color: #333;
            font-size: 1.1em;
        }
        
        .violation-card {
            background: #fff;
            border: 2px solid #ff6b6b;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
        }
        
        .violation-header {
            background: #ff6b6b;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px;
            font-size: 1.2em;
            font-weight: bold;
        }
        
        .violation-details {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }
        
        .no-violations {
            text-align: center;
            padding: 30px;
            color: #28a745;
            font-size: 1.2em;
            background: #d4edda;
            border-radius: 5px;
        }
        
        @media print {
            body {
                background: white;
                padding: 0;
            }
            
            .container {
                box-shadow: none;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>تقرير السيارة</h1>
            <h2>Vehicle Report</h2>
            <p>{{ current_date }}</p>
        </div>
        
        <div class="content">
            <!-- Vehicle Information -->
            <div class="section">
                <div class="section-title">بيانات السيارة - Vehicle Information</div>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">رقم اللوحة / Plate Number</div>
                        <div class="info-value">{{ vehicle.plate_number }}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">نوع السيارة / Type</div>
                        <div class="info-value">{{ vehicle.vehicle_type or 'غير محدد' }}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">الماركة / Make</div>
                        <div class="info-value">{{ vehicle.make or 'غير محدد' }}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">الموديل / Model</div>
                        <div class="info-value">{{ vehicle.model or 'غير محدد' }}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">السنة / Year</div>
                        <div class="info-value">{{ vehicle.year or 'غير محدد' }}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">اللون / Color</div>
                        <div class="info-value">{{ vehicle.color or 'غير محدد' }}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">رقم الملصق / Sticker Number</div>
                        <div class="info-value">{{ vehicle.sticker_number or 'غير محدد' }}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">عدد المخالفات / Violations Count</div>
                        <div class="info-value">{{ vehicle.violation_count }}</div>
                    </div>
                </div>
            </div>
            
            <!-- Owner Information -->
            <div class="section">
                <div class="section-title">بيانات المالك - Owner Information</div>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">اسم المالك / Owner Name</div>
                        <div class="info-value">{{ vehicle.owner_name or 'غير محدد' }}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">الرقم الوطني / National ID</div>
                        <div class="info-value">{{ vehicle.owner_national_id or 'غير محدد' }}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">الهاتف / Phone</div>
                        <div class="info-value">{{ vehicle.owner_phone or 'غير محدد' }}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">البريد الإلكتروني / Email</div>
                        <div class="info-value">{{ vehicle.owner_email or 'غير محدد' }}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">القسم / Department</div>
                        <div class="info-value">{{ vehicle.department or 'غير محدد' }}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">المسمى الوظيفي / Job Title</div>
                        <div class="info-value">{{ vehicle.job_title or 'غير محدد' }}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">رقم الوحدة / Unit Number</div>
                        <div class="info-value">{{ vehicle.unit_number or 'غير محدد' }}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">اسم المبنى / Building Name</div>
                        <div class="info-value">{{ vehicle.building_name or 'غير محدد' }}</div>
                    </div>
                </div>
            </div>
            
            <!-- Violations -->
            <div class="section">
                <div class="section-title">المخالفات المرورية - Traffic Violations ({{ vehicle.violations|length }})</div>
                
                {% if vehicle.violations %}
                    {% for violation in vehicle.violations %}
                    <div class="violation-card">
                        <div class="violation-header">مخالفة رقم {{ loop.index }} - Violation #{{ loop.index }}</div>
                        <div class="violation-details">
                            <div class="info-item">
                                <div class="info-label">نوع المخالفة / Type</div>
                                <div class="info-value">{{ violation.violation_type }}</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">التاريخ / Date</div>
                                <div class="info-value">{{ violation.violation_date }}</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">الموقع / Location</div>
                                <div class="info-value">{{ violation.location or 'غير محدد' }}</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">الغرامة / Fine</div>
                                <div class="info-value">{{ violation.fine_amount or 0 }} ريال</div>
                            </div>
                            <div class="info-item" style="grid-column: 1 / -1;">
                                <div class="info-label">الوصف / Description</div>
                                <div class="info-value">{{ violation.description or 'لا يوجد' }}</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">الحالة / Status</div>
                                <div class="info-value">{{ violation.status }}</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">المُبلِّغ / Reported By</div>
                                <div class="info-value">{{ violation.reported_by_name or 'غير محدد' }}</div>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                {% else %}
                    <div class="no-violations">
                        ✓ لا توجد مخالفات مسجلة لهذه السيارة<br>
                        No violations recorded for this vehicle
                    </div>
                {% endif %}
            </div>
        </div>
    </div>
</body>
</html>
        '''
        
        template = Template(template_str)
        html_content = template.render(
            vehicle=vehicle,
            current_date=datetime.now().strftime('%Y/%m/%d %H:%M')
        )
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return True
        
    except Exception as e:
        print(f"Error exporting vehicle to HTML: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def export_all_vehicles_to_html(vehicles: List[Dict], output_path: str) -> bool:
    """
    Export all vehicles report to HTML
    تصدير تقرير جميع السيارات إلى HTML
    
    Args:
        vehicles: List of vehicles
        output_path: Output file path
    
    Returns:
        True if successful
    """
    try:
        from jinja2 import Template
        
        template_str = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تقرير جميع السيارات</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(90deg, #0f3d68 60%, #2e8bc0 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2em;
            margin-bottom: 10px;
        }
        
        .content {
            padding: 30px;
        }
        
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .summary-card {
            background: #f8f9fa;
            border-right: 4px solid #2e8bc0;
            padding: 20px;
            border-radius: 5px;
        }
        
        .summary-card h3 {
            color: #0f3d68;
            margin-bottom: 10px;
        }
        
        .summary-card p {
            font-size: 2em;
            font-weight: bold;
            color: #2e8bc0;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        th {
            background: #2e8bc0;
            color: white;
            padding: 12px;
            text-align: center;
            font-weight: bold;
        }
        
        td {
            padding: 10px;
            text-align: center;
            border-bottom: 1px solid #ddd;
        }
        
        tr:nth-child(even) {
            background: #f8f9fa;
        }
        
        tr:hover {
            background: #e9ecef;
        }
        
        .badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: bold;
        }
        
        .badge-danger {
            background: #f8d7da;
            color: #721c24;
        }
        
        .badge-success {
            background: #d4edda;
            color: #155724;
        }
        
        @media print {
            body {
                background: white;
                padding: 0;
            }
            
            .container {
                box-shadow: none;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>تقرير جميع السيارات</h1>
            <h2>All Vehicles Report</h2>
            <p>{{ current_date }}</p>
        </div>
        
        <div class="content">
            <div class="summary">
                <div class="summary-card">
                    <h3>إجمالي السيارات<br>Total Vehicles</h3>
                    <p>{{ total_vehicles }}</p>
                </div>
                <div class="summary-card">
                    <h3>سيارات بمخالفات<br>With Violations</h3>
                    <p>{{ vehicles_with_violations }}</p>
                </div>
                <div class="summary-card">
                    <h3>إجمالي المخالفات<br>Total Violations</h3>
                    <p>{{ total_violations }}</p>
                </div>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>رقم اللوحة<br>Plate</th>
                        <th>النوع<br>Type</th>
                        <th>الماركة<br>Make</th>
                        <th>الموديل<br>Model</th>
                        <th>اللون<br>Color</th>
                        <th>رقم الملصق<br>Sticker</th>
                        <th>المالك<br>Owner</th>
                        <th>الوحدة<br>Unit</th>
                        <th>المخالفات<br>Violations</th>
                    </tr>
                </thead>
                <tbody>
                    {% for vehicle in vehicles %}
                    <tr>
                        <td>{{ loop.index }}</td>
                        <td><strong>{{ vehicle.plate_number }}</strong></td>
                        <td>{{ vehicle.vehicle_type or '-' }}</td>
                        <td>{{ vehicle.make or '-' }}</td>
                        <td>{{ vehicle.model or '-' }}</td>
                        <td>{{ vehicle.color or '-' }}</td>
                        <td>{{ vehicle.sticker_number or '-' }}</td>
                        <td>{{ vehicle.owner_name or '-' }}</td>
                        <td>{{ vehicle.unit_number or '-' }}</td>
                        <td>
                            {% if vehicle.violation_count > 0 %}
                            <span class="badge badge-danger">{{ vehicle.violation_count }}</span>
                            {% else %}
                            <span class="badge badge-success">0</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
        '''
        
        template = Template(template_str)
        
        total_vehicles = len(vehicles)
        vehicles_with_violations = sum(1 for v in vehicles if v.get('violation_count', 0) > 0)
        total_violations = sum(v.get('violation_count', 0) for v in vehicles)
        
        html_content = template.render(
            vehicles=vehicles,
            current_date=datetime.now().strftime('%Y/%m/%d %H:%M'),
            total_vehicles=total_vehicles,
            vehicles_with_violations=vehicles_with_violations,
            total_violations=total_violations
        )
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return True
        
    except Exception as e:
        print(f"Error exporting all vehicles to HTML: {str(e)}")
        return False
