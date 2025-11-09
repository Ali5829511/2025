"""
Plate Recognition & Violation Detection Integration
نظام متكامل للتعرف على اللوحات وكشف المخالفات المتكررة

This module integrates Plate Recognizer API with the traffic violations database
to automatically detect and track repeat offenders.

يتكامل هذا النظام مع خدمة Plate Recognizer وقاعدة بيانات المخالفات
للكشف التلقائي عن السيارات المخالفة والمتكررة.
"""

import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import database
import plate_recognizer


class ViolationDetector:
    """
    Automatic violation detection system using plate recognition
    نظام الكشف التلقائي عن المخالفات باستخدام التعرف على اللوحات
    """
    
    def __init__(self):
        """Initialize the violation detector"""
        self.api_configured = plate_recognizer.is_configured()
    
    def process_vehicle_image(self, image_path: str, user_id: int, 
                             location: Optional[str] = None,
                             auto_detect_violations: bool = True) -> Dict:
        """
        Process vehicle image and check for violations
        معالجة صورة المركبة والتحقق من المخالفات
        
        Args:
            image_path: Path to the vehicle image
            user_id: ID of the user processing the image
            location: Optional location where image was taken
            auto_detect_violations: Automatically check for repeat violations
        
        Returns:
            Dict containing:
            {
                'success': bool,
                'plate_number': str,
                'confidence': float,
                'vehicle_id': int (if found in database),
                'violation_history': List[Dict] (if vehicle has violations),
                'is_repeat_offender': bool,
                'violation_count': int,
                'recommendations': List[str]
            }
        """
        if not self.api_configured:
            return {
                'success': False,
                'error': 'Plate Recognizer API not configured',
                'error_ar': 'خدمة Plate Recognizer غير مفعلة'
            }
        
        # Step 1: Recognize plate from image
        recognition_result = plate_recognizer.recognize_plate_from_file(
            image_path, 
            regions=['sa']  # Saudi Arabia region
        )
        
        if not recognition_result.get('success'):
            return recognition_result
        
        results = recognition_result.get('results', [])
        if not results:
            return {
                'success': False,
                'error': 'No license plate detected in image',
                'error_ar': 'لم يتم اكتشاف لوحة سيارة في الصورة'
            }
        
        # Get the best result (highest confidence)
        best_result = max(results, key=lambda x: x.get('confidence', 0))
        plate_number = best_result.get('plate', '')
        confidence = best_result.get('confidence', 0)
        
        # Step 2: Search for vehicle in database
        vehicle = self._find_vehicle_by_plate(plate_number)
        vehicle_id = vehicle['id'] if vehicle else None
        
        # Step 3: Log the recognition event
        plate_recognizer.log_plate_recognition(
            user_id=user_id,
            plate_number=plate_number,
            confidence=confidence,
            vehicle_id=vehicle_id,
            image_path=image_path
        )
        
        result = {
            'success': True,
            'plate_number': plate_number,
            'confidence': confidence,
            'vehicle_id': vehicle_id,
            'vehicle_found': vehicle is not None
        }
        
        # Step 4: Check violation history if requested
        if auto_detect_violations and vehicle_id:
            violation_analysis = self._analyze_violations(vehicle_id)
            result.update(violation_analysis)
        
        return result
    
    def _find_vehicle_by_plate(self, plate_number: str) -> Optional[Dict]:
        """
        Find vehicle in database by plate number
        البحث عن المركبة في قاعدة البيانات برقم اللوحة
        
        Args:
            plate_number: Plate number to search for
        
        Returns:
            Dict with vehicle info or None if not found
        """
        try:
            conn = database.get_db_connection()
            cursor = conn.cursor()
            
            # Search for exact match or similar plates
            cursor.execute('''
                SELECT * FROM vehicles 
                WHERE LOWER(REPLACE(plate_number, ' ', '')) = LOWER(REPLACE(?, ' ', ''))
                LIMIT 1
            ''', (plate_number,))
            
            vehicle = cursor.fetchone()
            conn.close()
            
            return dict(vehicle) if vehicle else None
        
        except Exception as e:
            print(f"Error finding vehicle: {str(e)}")
            return None
    
    def _analyze_violations(self, vehicle_id: int) -> Dict:
        """
        Analyze violation history for a vehicle
        تحليل سجل المخالفات للمركبة
        
        Args:
            vehicle_id: ID of the vehicle
        
        Returns:
            Dict with violation analysis
        """
        try:
            conn = database.get_db_connection()
            cursor = conn.cursor()
            
            # Get all violations for this vehicle
            cursor.execute('''
                SELECT * FROM traffic_violations 
                WHERE vehicle_id = ?
                ORDER BY violation_date DESC
            ''', (vehicle_id,))
            
            violations = [dict(row) for row in cursor.fetchall()]
            
            # Count violations in last 30 days
            thirty_days_ago = datetime.now() - timedelta(days=30)
            recent_violations = [
                v for v in violations 
                if datetime.fromisoformat(v['violation_date']) > thirty_days_ago
            ]
            
            # Count violations in last 90 days
            ninety_days_ago = datetime.now() - timedelta(days=90)
            quarterly_violations = [
                v for v in violations 
                if datetime.fromisoformat(v['violation_date']) > ninety_days_ago
            ]
            
            conn.close()
            
            # Determine if repeat offender
            total_violations = len(violations)
            is_repeat_offender = total_violations >= 3
            is_frequent_offender = len(recent_violations) >= 2
            is_serious_offender = len(quarterly_violations) >= 5
            
            # Generate recommendations
            recommendations = []
            recommendations_ar = []
            
            if is_serious_offender:
                recommendations.append("SERIOUS OFFENDER: Consider vehicle immobilization")
                recommendations_ar.append("مخالف خطير: يُنصح بتثبيت المركبة")
            elif is_frequent_offender:
                recommendations.append("FREQUENT OFFENDER: Escalate to management")
                recommendations_ar.append("مخالف متكرر: إحالة للإدارة")
            elif is_repeat_offender:
                recommendations.append("REPEAT OFFENDER: Send warning notice")
                recommendations_ar.append("مخالف متكرر: إرسال إنذار")
            else:
                recommendations.append("First-time or occasional offender")
                recommendations_ar.append("مخالف للمرة الأولى أو بشكل عرضي")
            
            return {
                'violation_history': violations[:10],  # Last 10 violations
                'total_violations': total_violations,
                'recent_violations_30d': len(recent_violations),
                'recent_violations_90d': len(quarterly_violations),
                'is_repeat_offender': is_repeat_offender,
                'is_frequent_offender': is_frequent_offender,
                'is_serious_offender': is_serious_offender,
                'recommendations': recommendations,
                'recommendations_ar': recommendations_ar,
                'last_violation_date': violations[0]['violation_date'] if violations else None
            }
        
        except Exception as e:
            print(f"Error analyzing violations: {str(e)}")
            return {
                'error': str(e),
                'violation_history': [],
                'total_violations': 0,
                'is_repeat_offender': False
            }
    
    def get_repeat_offenders(self, min_violations: int = 3, 
                           days_period: int = 90) -> List[Dict]:
        """
        Get list of repeat offenders
        الحصول على قائمة المخالفين المتكررين
        
        Args:
            min_violations: Minimum number of violations to be considered repeat offender
            days_period: Time period in days to check
        
        Returns:
            List of vehicles with repeat violations
        """
        try:
            conn = database.get_db_connection()
            cursor = conn.cursor()
            
            cutoff_date = datetime.now() - timedelta(days=days_period)
            
            cursor.execute('''
                SELECT 
                    v.id,
                    v.plate_number,
                    v.owner_name,
                    v.make,
                    v.model,
                    COUNT(tv.id) as violation_count,
                    MAX(tv.violation_date) as last_violation,
                    SUM(tv.fine_amount) as total_fines
                FROM vehicles v
                INNER JOIN traffic_violations tv ON v.id = tv.vehicle_id
                WHERE tv.violation_date > ?
                GROUP BY v.id, v.plate_number, v.owner_name, v.make, v.model
                HAVING COUNT(tv.id) >= ?
                ORDER BY violation_count DESC, last_violation DESC
            ''', (cutoff_date, min_violations))
            
            offenders = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return offenders
        
        except Exception as e:
            print(f"Error getting repeat offenders: {str(e)}")
            return []
    
    def auto_record_violation(self, vehicle_id: int, violation_type: str,
                            location: Optional[str] = None,
                            description: Optional[str] = None,
                            fine_amount: Optional[float] = None,
                            user_id: Optional[int] = None) -> Dict:
        """
        Automatically record a traffic violation
        تسجيل مخالفة مرورية تلقائياً
        
        Args:
            vehicle_id: ID of the vehicle
            violation_type: Type of violation
            location: Where the violation occurred
            description: Description of the violation
            fine_amount: Fine amount
            user_id: User who reported the violation
        
        Returns:
            Dict with result of the operation
        """
        try:
            conn = database.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO traffic_violations 
                (vehicle_id, violation_type, violation_date, location, 
                 description, fine_amount, status, reported_by)
                VALUES (?, ?, ?, ?, ?, ?, 'pending', ?)
            ''', (vehicle_id, violation_type, datetime.now(), location,
                  description, fine_amount, user_id))
            
            violation_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Log audit trail
            if user_id:
                database.log_audit(
                    user_id,
                    f'Auto-recorded violation for vehicle ID {vehicle_id}: {violation_type}',
                    details=f'Violation ID: {violation_id}'
                )
            
            return {
                'success': True,
                'violation_id': violation_id,
                'message': 'Violation recorded successfully',
                'message_ar': 'تم تسجيل المخالفة بنجاح'
            }
        
        except Exception as e:
            print(f"Error recording violation: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'error_ar': f'خطأ في تسجيل المخالفة: {str(e)}'
            }


# Global instance
detector = ViolationDetector()


def process_vehicle_image(image_path: str, user_id: int, **kwargs) -> Dict:
    """
    Convenience function to process vehicle image
    دالة سريعة لمعالجة صورة المركبة
    """
    return detector.process_vehicle_image(image_path, user_id, **kwargs)


def get_repeat_offenders(**kwargs) -> List[Dict]:
    """
    Convenience function to get repeat offenders
    دالة سريعة للحصول على المخالفين المتكررين
    """
    return detector.get_repeat_offenders(**kwargs)


def auto_record_violation(vehicle_id: int, violation_type: str, **kwargs) -> Dict:
    """
    Convenience function to auto-record violation
    دالة سريعة لتسجيل المخالفة تلقائياً
    """
    return detector.auto_record_violation(vehicle_id, violation_type, **kwargs)
