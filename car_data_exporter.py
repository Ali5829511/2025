"""
Car Data Exporter Module
نظام تصدير بيانات السيارات

This module provides professional export functionality for car analysis data:
- Excel (XLSX) export with formatting and thumbnails
- PDF export with images
- HTML export
"""

import os
from datetime import datetime
from typing import List, Dict, Optional
import database
from io import BytesIO
from PIL import Image


def export_to_excel(analysis_records: List[Dict], output_path: str) -> bool:
    """
    Export car analysis data to Excel with professional formatting
    تصدير بيانات تحليل السيارات إلى Excel بتنسيق احترافي
    
    Args:
        analysis_records: List of analysis record dicts
        output_path: Path to save Excel file
    
    Returns:
        bool: True if successful
    """
    try:
        import xlsxwriter
        
        workbook = xlsxwriter.Workbook(output_path)
        worksheet = workbook.add_worksheet('تحليل السيارات')
        
        # Set RTL mode for Arabic
        worksheet.right_to_left()
        
        # Define formats
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 16,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#0f3d68',
            'font_color': 'white',
            'border': 1
        })
        
        header_format = workbook.add_format({
            'bold': True,
            'font_size': 12,
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
        
        date_format = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'num_format': 'dd/mm/yyyy hh:mm'
        })
        
        # Set column widths
        worksheet.set_column('A:A', 15)  # Thumbnail
        worksheet.set_column('B:B', 20)  # Plate number
        worksheet.set_column('C:C', 15)  # Vehicle type
        worksheet.set_column('D:D', 15)  # Color
        worksheet.set_column('E:E', 12)  # Confidence
        worksheet.set_column('F:F', 12)  # Violations
        worksheet.set_column('G:G', 20)  # Owner
        worksheet.set_column('H:H', 20)  # Date
        
        # Write title
        current_date = datetime.now().strftime('%Y/%m/%d %H:%M')
        worksheet.merge_range('A1:H1', f'تقرير تحليل السيارات - {current_date}', title_format)
        
        # Write headers
        headers = [
            'صورة مصغرة',
            'رقم اللوحة',
            'نوع السيارة',
            'اللون',
            'دقة التعرف',
            'عدد المخالفات',
            'المالك',
            'تاريخ التحليل'
        ]
        
        for col, header in enumerate(headers):
            worksheet.write(1, col, header, header_format)
        
        # Set row height for header and title
        worksheet.set_row(0, 30)
        worksheet.set_row(1, 25)
        
        # Write data
        for idx, record in enumerate(analysis_records):
            row = idx + 2
            
            # Set row height for images
            worksheet.set_row(row, 60)
            
            # Insert thumbnail if available
            if record.get('thumbnail_path') and os.path.exists(record['thumbnail_path']):
                try:
                    worksheet.insert_image(row, 0, record['thumbnail_path'], {
                        'x_scale': 0.5,
                        'y_scale': 0.5,
                        'x_offset': 5,
                        'y_offset': 5
                    })
                except:
                    worksheet.write(row, 0, 'لا توجد صورة', cell_format)
            else:
                worksheet.write(row, 0, 'لا توجد صورة', cell_format)
            
            # Write data cells
            worksheet.write(row, 1, record.get('plate_number', 'غير محدد'), cell_format)
            worksheet.write(row, 2, record.get('vehicle_type', 'غير محدد'), cell_format)
            worksheet.write(row, 3, record.get('vehicle_color', 'غير محدد'), cell_format)
            
            confidence = record.get('plate_confidence', 0)
            worksheet.write(row, 4, f"{confidence:.2%}" if confidence else '-', cell_format)
            
            worksheet.write(row, 5, record.get('violation_count', 0), cell_format)
            worksheet.write(row, 6, record.get('owner_name', 'غير معروف'), cell_format)
            
            analysis_date = record.get('analysis_date', '')
            if analysis_date:
                try:
                    date_obj = datetime.fromisoformat(analysis_date)
                    worksheet.write_datetime(row, 7, date_obj, date_format)
                except:
                    worksheet.write(row, 7, analysis_date, cell_format)
            else:
                worksheet.write(row, 7, '-', cell_format)
        
        workbook.close()
        return True
        
    except Exception as e:
        print(f"Error exporting to Excel: {str(e)}")
        return False


def export_to_pdf(analysis_records: List[Dict], output_path: str) -> bool:
    """
    Export car analysis data to PDF with professional formatting
    تصدير بيانات تحليل السيارات إلى PDF بتنسيق احترافي
    
    Args:
        analysis_records: List of analysis record dicts
        output_path: Path to save PDF file
    
    Returns:
        bool: True if successful
    """
    try:
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.enums import TA_CENTER, TA_RIGHT
        
        # Create PDF
        doc = SimpleDocTemplate(
            output_path,
            pagesize=landscape(A4),
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=30
        )
        
        elements = []
        
        # Try to register Arabic font (optional, falls back to default if not available)
        try:
            # This would need an Arabic font file - skipping for now
            pass
        except:
            pass
        
        # Create title
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#0f3d68'),
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        current_date = datetime.now().strftime('%Y/%m/%d %H:%M')
        title = Paragraph(f'Car Analysis Report - تقرير تحليل السيارات<br/>{current_date}', title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.3*inch))
        
        # Prepare table data
        table_data = [[
            'Thumbnail\nصورة',
            'Plate\nرقم اللوحة',
            'Type\nالنوع',
            'Color\nاللون',
            'Confidence\nالدقة',
            'Violations\nمخالفات',
            'Owner\nالمالك',
            'Date\nالتاريخ'
        ]]
        
        for record in analysis_records:
            row = []
            
            # Add thumbnail
            if record.get('thumbnail_path') and os.path.exists(record['thumbnail_path']):
                try:
                    img = RLImage(record['thumbnail_path'], width=0.8*inch, height=0.6*inch)
                    row.append(img)
                except:
                    row.append('No Image')
            else:
                row.append('No Image')
            
            # Add data
            row.append(record.get('plate_number', 'N/A'))
            row.append(record.get('vehicle_type', 'N/A'))
            row.append(record.get('vehicle_color', 'N/A'))
            
            confidence = record.get('plate_confidence', 0)
            row.append(f"{confidence:.1%}" if confidence else '-')
            
            row.append(str(record.get('violation_count', 0)))
            row.append(record.get('owner_name', 'Unknown'))
            
            analysis_date = record.get('analysis_date', '')
            if analysis_date:
                try:
                    date_obj = datetime.fromisoformat(analysis_date)
                    row.append(date_obj.strftime('%Y/%m/%d\n%H:%M'))
                except:
                    row.append(analysis_date)
            else:
                row.append('-')
            
            table_data.append(row)
        
        # Create table
        table = Table(table_data, colWidths=[1*inch, 1.2*inch, 1*inch, 1*inch, 0.8*inch, 0.8*inch, 1.2*inch, 1*inch])
        
        # Style table
        table.setStyle(TableStyle([
            # Header style
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e8bc0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Data style
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
        ]))
        
        elements.append(table)
        
        # Build PDF
        doc.build(elements)
        return True
        
    except Exception as e:
        print(f"Error exporting to PDF: {str(e)}")
        return False


def export_to_html(analysis_records: List[Dict], output_path: str) -> bool:
    """
    Export car analysis data to HTML with professional formatting
    تصدير بيانات تحليل السيارات إلى HTML بتنسيق احترافي
    
    Args:
        analysis_records: List of analysis record dicts
        output_path: Path to save HTML file
    
    Returns:
        bool: True if successful
    """
    try:
        from jinja2 import Template
        
        html_template = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تقرير تحليل السيارات - Car Analysis Report</title>
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
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
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
            border-left: 4px solid #2e8bc0;
            padding: 20px;
            border-radius: 5px;
        }
        
        .summary-card h3 {
            color: #0f3d68;
            margin-bottom: 10px;
            font-size: 0.9em;
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
            padding: 15px;
            text-align: center;
            font-weight: bold;
        }
        
        td {
            padding: 12px;
            text-align: center;
            border-bottom: 1px solid #ddd;
        }
        
        tr:nth-child(even) {
            background: #f8f9fa;
        }
        
        tr:hover {
            background: #e9ecef;
        }
        
        .thumbnail {
            width: 100px;
            height: 75px;
            object-fit: cover;
            border-radius: 5px;
        }
        
        .badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: bold;
        }
        
        .badge-success {
            background: #d4edda;
            color: #155724;
        }
        
        .badge-warning {
            background: #fff3cd;
            color: #856404;
        }
        
        .badge-danger {
            background: #f8d7da;
            color: #721c24;
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
            <h1>تقرير تحليل السيارات</h1>
            <h1>Car Analysis Report</h1>
            <p>{{ current_date }}</p>
        </div>
        
        <div class="content">
            <div class="summary">
                <div class="summary-card">
                    <h3>إجمالي السيارات / Total Cars</h3>
                    <p>{{ total_cars }}</p>
                </div>
                <div class="summary-card">
                    <h3>سيارات مسجلة / Registered</h3>
                    <p>{{ registered_cars }}</p>
                </div>
                <div class="summary-card">
                    <h3>سيارات غير مسجلة / Unregistered</h3>
                    <p>{{ unregistered_cars }}</p>
                </div>
                <div class="summary-card">
                    <h3>إجمالي المخالفات / Total Violations</h3>
                    <p>{{ total_violations }}</p>
                </div>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>صورة<br>Thumbnail</th>
                        <th>رقم اللوحة<br>Plate Number</th>
                        <th>نوع السيارة<br>Vehicle Type</th>
                        <th>اللون<br>Color</th>
                        <th>دقة التعرف<br>Confidence</th>
                        <th>المخالفات<br>Violations</th>
                        <th>المالك<br>Owner</th>
                        <th>التاريخ<br>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {% for record in records %}
                    <tr>
                        <td>
                            {% if record.thumbnail_path %}
                            <img src="{{ record.thumbnail_path }}" alt="Car" class="thumbnail">
                            {% else %}
                            <span style="color: #999;">لا توجد صورة</span>
                            {% endif %}
                        </td>
                        <td><strong>{{ record.plate_number }}</strong></td>
                        <td>{{ record.vehicle_type }}</td>
                        <td>{{ record.vehicle_color }}</td>
                        <td>
                            {% if record.plate_confidence >= 0.8 %}
                            <span class="badge badge-success">{{ "%.0f"|format(record.plate_confidence * 100) }}%</span>
                            {% elif record.plate_confidence >= 0.5 %}
                            <span class="badge badge-warning">{{ "%.0f"|format(record.plate_confidence * 100) }}%</span>
                            {% else %}
                            <span class="badge badge-danger">{{ "%.0f"|format(record.plate_confidence * 100) }}%</span>
                            {% endif %}
                        </td>
                        <td>
                            {% if record.violation_count > 0 %}
                            <span class="badge badge-danger">{{ record.violation_count }}</span>
                            {% else %}
                            <span class="badge badge-success">0</span>
                            {% endif %}
                        </td>
                        <td>{{ record.owner_name or 'غير معروف / Unknown' }}</td>
                        <td>{{ record.analysis_date }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
        '''
        
        # Calculate summary statistics
        total_cars = len(analysis_records)
        registered_cars = sum(1 for r in analysis_records if r.get('owner_name'))
        unregistered_cars = total_cars - registered_cars
        total_violations = sum(r.get('violation_count', 0) for r in analysis_records)
        
        # Render template
        template = Template(html_template)
        html_content = template.render(
            current_date=datetime.now().strftime('%Y/%m/%d %H:%M'),
            total_cars=total_cars,
            registered_cars=registered_cars,
            unregistered_cars=unregistered_cars,
            total_violations=total_violations,
            records=analysis_records
        )
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return True
        
    except Exception as e:
        print(f"Error exporting to HTML: {str(e)}")
        return False


def get_car_analysis_records(filter_params: Optional[Dict] = None) -> List[Dict]:
    """
    Get car analysis records from database
    الحصول على سجلات تحليل السيارات من قاعدة البيانات
    
    Args:
        filter_params: Optional filter parameters
    
    Returns:
        List of analysis record dicts
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                ca.*,
                ci.original_filename,
                ci.image_path,
                ci.thumbnail_path,
                v.plate_number as registered_plate,
                r.name as owner_name,
                r.phone as owner_phone,
                r.unit_number as owner_unit
            FROM car_analysis ca
            LEFT JOIN car_images ci ON ca.car_image_id = ci.id
            LEFT JOIN vehicles v ON ca.vehicle_id = v.id
            LEFT JOIN residents r ON v.owner_id = r.id
            ORDER BY ca.analysis_date DESC
        '''
        
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        records = []
        for row in rows:
            record = dict(row)
            # Format date for display
            if record.get('analysis_date'):
                try:
                    date_obj = datetime.fromisoformat(record['analysis_date'])
                    record['analysis_date'] = date_obj.strftime('%Y/%m/%d %H:%M')
                except:
                    pass
            records.append(record)
        
        return records
        
    except Exception as e:
        print(f"Error getting car analysis records: {str(e)}")
        return []
