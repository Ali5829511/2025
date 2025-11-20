"""
API Token Management Module
نظام إدارة رموز الوصول للواجهة البرمجية

This module provides functionality for:
- Creating and managing API tokens
- Validating API tokens
- Tracking token usage
- Revoking tokens
"""

import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import database


def generate_token() -> str:
    """
    Generate a secure random API token
    توليد رمز وصول عشوائي آمن
    
    Returns:
        str: 64-character hexadecimal token
    """
    # Generate 32 random bytes and convert to hex (64 characters)
    return secrets.token_hex(32)


def hash_token(token: str) -> str:
    """
    Hash a token for secure storage
    تشفير رمز الوصول للتخزين الآمن
    
    Args:
        token: Plain text token
    
    Returns:
        str: SHA256 hash of the token
    """
    return hashlib.sha256(token.encode()).hexdigest()


def create_api_token(
    name: str,
    user_id: int,
    created_by: int,
    description: str = '',
    permissions: str = 'read',
    expires_days: Optional[int] = None
) -> Dict:
    """
    Create a new API token
    إنشاء رمز وصول جديد
    
    Args:
        name: Token name/label
        user_id: User ID this token belongs to
        created_by: User ID who created the token
        description: Optional description
        permissions: Comma-separated permissions (e.g., 'read,write')
        expires_days: Days until expiration (None = never expires)
    
    Returns:
        Dict with token information
    """
    try:
        # Generate token
        token = generate_token()
        token_hash = hash_token(token)
        
        # Calculate expiration date
        expires_at = None
        if expires_days:
            expires_at = (datetime.now() + timedelta(days=expires_days)).isoformat()
        
        # Store in database
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO api_tokens 
            (token, name, user_id, description, permissions, expires_at, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (token_hash, name, user_id, description, permissions, expires_at, created_by))
        
        token_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            'success': True,
            'token_id': token_id,
            'token': token,  # Return plain token only once
            'token_hash': token_hash,
            'name': name,
            'permissions': permissions,
            'expires_at': expires_at,
            'message': 'API token created successfully',
            'message_ar': 'تم إنشاء رمز الوصول بنجاح',
            'warning': 'Save this token now. You will not be able to see it again.',
            'warning_ar': 'احفظ هذا الرمز الآن. لن تتمكن من رؤيته مرة أخرى.'
        }
    
    except Exception as e:
        print(f"Error creating API token: {e}")
        return {
            'success': False,
            'error': 'Failed to create API token',
            'error_ar': 'فشل إنشاء رمز الوصول'
        }


def validate_api_token(token: str) -> Optional[Dict]:
    """
    Validate an API token and return associated user info
    التحقق من صحة رمز الوصول
    
    Args:
        token: Plain text token to validate
    
    Returns:
        Dict with user info if valid, None if invalid
    """
    try:
        token_hash = hash_token(token)
        
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                t.id, t.user_id, t.name, t.permissions, t.expires_at, t.is_active,
                u.username, u.role, u.is_active as user_is_active
            FROM api_tokens t
            JOIN users u ON t.user_id = u.id
            WHERE t.token = ? AND t.is_active = 1
        ''', (token_hash,))
        
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        token_data = dict(row)
        
        # Check if token expired
        if token_data['expires_at']:
            expires_at = datetime.fromisoformat(token_data['expires_at'])
            if datetime.now() > expires_at:
                conn.close()
                return None
        
        # Check if user is active
        if not token_data['user_is_active']:
            conn.close()
            return None
        
        # Update last_used timestamp
        cursor.execute('''
            UPDATE api_tokens 
            SET last_used = CURRENT_TIMESTAMP 
            WHERE id = ?
        ''', (token_data['id'],))
        
        conn.commit()
        conn.close()
        
        return {
            'token_id': token_data['id'],
            'user_id': token_data['user_id'],
            'username': token_data['username'],
            'role': token_data['role'],
            'permissions': token_data['permissions'].split(',') if token_data['permissions'] else [],
            'token_name': token_data['name']
        }
    
    except Exception as e:
        print(f"Error validating API token: {e}")
        return None


def log_token_usage(
    token_id: int,
    endpoint: str,
    method: str,
    ip_address: str,
    user_agent: str,
    status_code: int,
    response_time_ms: int = 0
) -> bool:
    """
    Log API token usage
    تسجيل استخدام رمز الوصول
    
    Args:
        token_id: Token ID
        endpoint: API endpoint accessed
        method: HTTP method
        ip_address: Client IP address
        user_agent: Client user agent
        status_code: HTTP status code
        response_time_ms: Response time in milliseconds
    
    Returns:
        bool: True if logged successfully
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO api_token_usage
            (token_id, endpoint, method, ip_address, user_agent, status_code, response_time_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (token_id, endpoint, method, ip_address, user_agent, status_code, response_time_ms))
        
        conn.commit()
        conn.close()
        
        return True
    
    except Exception as e:
        print(f"Error logging token usage: {e}")
        return False


def list_api_tokens(user_id: Optional[int] = None, include_inactive: bool = False) -> List[Dict]:
    """
    List all API tokens
    عرض قائمة رموز الوصول
    
    Args:
        user_id: Optional filter by user ID
        include_inactive: Whether to include inactive tokens
    
    Returns:
        List of token information dicts
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                t.id, t.name, t.user_id, t.description, t.permissions,
                t.is_active, t.last_used, t.expires_at, t.created_at,
                u.username, u.role
            FROM api_tokens t
            JOIN users u ON t.user_id = u.id
            WHERE 1=1
        '''
        params = []
        
        if user_id:
            query += ' AND t.user_id = ?'
            params.append(user_id)
        
        if not include_inactive:
            query += ' AND t.is_active = 1'
        
        query += ' ORDER BY t.created_at DESC'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        tokens = []
        for row in rows:
            token_data = dict(row)
            
            # Check if expired
            is_expired = False
            if token_data['expires_at']:
                expires_at = datetime.fromisoformat(token_data['expires_at'])
                is_expired = datetime.now() > expires_at
            
            tokens.append({
                'id': token_data['id'],
                'name': token_data['name'],
                'user_id': token_data['user_id'],
                'username': token_data['username'],
                'user_role': token_data['role'],
                'description': token_data['description'],
                'permissions': token_data['permissions'],
                'is_active': token_data['is_active'],
                'is_expired': is_expired,
                'last_used': token_data['last_used'],
                'expires_at': token_data['expires_at'],
                'created_at': token_data['created_at']
            })
        
        return tokens
    
    except Exception as e:
        print(f"Error listing API tokens: {e}")
        return []


def revoke_api_token(token_id: int, revoked_by: int) -> Dict:
    """
    Revoke (deactivate) an API token
    إلغاء رمز الوصول
    
    Args:
        token_id: Token ID to revoke
        revoked_by: User ID who revoked the token
    
    Returns:
        Dict with operation result
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE api_tokens 
            SET is_active = 0 
            WHERE id = ?
        ''', (token_id,))
        
        if cursor.rowcount == 0:
            conn.close()
            return {
                'success': False,
                'error': 'Token not found',
                'error_ar': 'الرمز غير موجود'
            }
        
        conn.commit()
        
        # Log the revocation
        database.log_audit(
            revoked_by,
            f'API token revoked: ID {token_id}'
        )
        
        conn.close()
        
        return {
            'success': True,
            'message': 'API token revoked successfully',
            'message_ar': 'تم إلغاء رمز الوصول بنجاح'
        }
    
    except Exception as e:
        print(f"Error revoking API token: {e}")
        return {
            'success': False,
            'error': 'Failed to revoke API token',
            'error_ar': 'فشل إلغاء رمز الوصول'
        }


def get_token_usage_stats(token_id: int, days: int = 30) -> Dict:
    """
    Get usage statistics for a token
    الحصول على إحصائيات استخدام الرمز
    
    Args:
        token_id: Token ID
        days: Number of days to look back
    
    Returns:
        Dict with usage statistics
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        since_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        # Total requests
        cursor.execute('''
            SELECT COUNT(*) as total_requests,
                   AVG(response_time_ms) as avg_response_time,
                   COUNT(CASE WHEN status_code >= 200 AND status_code < 300 THEN 1 END) as successful_requests,
                   COUNT(CASE WHEN status_code >= 400 THEN 1 END) as failed_requests
            FROM api_token_usage
            WHERE token_id = ? AND request_time >= ?
        ''', (token_id, since_date))
        
        stats = dict(cursor.fetchone())
        
        # Requests by endpoint
        cursor.execute('''
            SELECT endpoint, COUNT(*) as count
            FROM api_token_usage
            WHERE token_id = ? AND request_time >= ?
            GROUP BY endpoint
            ORDER BY count DESC
        ''', (token_id, since_date))
        
        endpoints = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            'success': True,
            'token_id': token_id,
            'period_days': days,
            'total_requests': stats['total_requests'] or 0,
            'successful_requests': stats['successful_requests'] or 0,
            'failed_requests': stats['failed_requests'] or 0,
            'avg_response_time_ms': round(stats['avg_response_time'] or 0, 2),
            'endpoints': endpoints
        }
    
    except Exception as e:
        print(f"Error getting token usage stats: {e}")
        return {
            'success': False,
            'error': 'Failed to get token usage statistics',
            'error_ar': 'فشل الحصول على إحصائيات استخدام الرمز'
        }
