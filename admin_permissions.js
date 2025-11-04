// نظام التحقق من صلاحيات المدير
class AdminPermissions {
    constructor() {
        this.currentUser = this.getCurrentUser();
        this.initializePermissions();
    }

    // الحصول على بيانات المستخدم الحالي
    getCurrentUser() {
        // في التطبيق الحقيقي، سيتم الحصول على هذه البيانات من الخادم
        // هنا نستخدم localStorage كمثال
        const userData = localStorage.getItem('currentUser');
        if (userData) {
            return JSON.parse(userData);
        }
        
        // افتراضي: المستخدم admin له صلاحيات كاملة
        return {
            username: 'admin',
            role: 'admin',
            permissions: ['read', 'write', 'edit', 'delete', 'admin']
        };
    }

    // التحقق من صلاحية المدير
    isAdmin() {
        return this.currentUser && 
               (this.currentUser.role === 'admin' || 
                this.currentUser.permissions.includes('admin'));
    }

    // التحقق من صلاحية التعديل
    canEdit() {
        return this.currentUser && 
               (this.currentUser.permissions.includes('edit') || 
                this.currentUser.permissions.includes('admin'));
    }

    // التحقق من صلاحية الحذف
    canDelete() {
        return this.currentUser && 
               (this.currentUser.permissions.includes('delete') || 
                this.currentUser.permissions.includes('admin'));
    }

    // إظهار أو إخفاء أزرار التعديل والحذف
    initializePermissions() {
        document.addEventListener('DOMContentLoaded', () => {
            this.setupEditDeleteButtons();
            this.setupAdminOnlyElements();
        });
    }

    // إعداد أزرار التعديل والحذف
    setupEditDeleteButtons() {
        const editButtons = document.querySelectorAll('.edit-btn, .btn-edit');
        const deleteButtons = document.querySelectorAll('.delete-btn, .btn-delete');
        const adminOnlyButtons = document.querySelectorAll('.admin-only');

        // إظهار/إخفاء أزرار التعديل
        editButtons.forEach(button => {
            if (this.canEdit()) {
                button.style.display = 'inline-block';
                button.disabled = false;
            } else {
                button.style.display = 'none';
                button.disabled = true;
            }
        });

        // إظهار/إخفاء أزرار الحذف
        deleteButtons.forEach(button => {
            if (this.canDelete()) {
                button.style.display = 'inline-block';
                button.disabled = false;
            } else {
                button.style.display = 'none';
                button.disabled = true;
            }
        });

        // إظهار/إخفاء العناصر الخاصة بالمدير فقط
        adminOnlyButtons.forEach(button => {
            if (this.isAdmin()) {
                button.style.display = 'inline-block';
                button.disabled = false;
            } else {
                button.style.display = 'none';
                button.disabled = true;
            }
        });
    }

    // إعداد العناصر الخاصة بالمدير فقط
    setupAdminOnlyElements() {
        const adminOnlyElements = document.querySelectorAll('.admin-only-section');
        
        adminOnlyElements.forEach(element => {
            if (this.isAdmin()) {
                element.style.display = 'block';
            } else {
                element.style.display = 'none';
            }
        });
    }

    // إضافة أزرار التعديل والحذف لصف في الجدول
    addEditDeleteButtons(row, itemId, itemType) {
        if (!this.isAdmin()) {
            return;
        }

        const actionsCell = row.querySelector('.actions-cell') || row.cells[row.cells.length - 1];
        
        // إنشاء أزرار التعديل والحذف
        const editButton = this.createEditButton(itemId, itemType);
        const deleteButton = this.createDeleteButton(itemId, itemType);
        
        // إضافة الأزرار للخلية
        actionsCell.innerHTML = '';
        actionsCell.appendChild(editButton);
        actionsCell.appendChild(deleteButton);
    }

    // إنشاء زر التعديل
    createEditButton(itemId, itemType) {
        const button = document.createElement('button');
        button.className = 'btn btn-sm btn-warning edit-btn';
        button.innerHTML = '<i class="fas fa-edit"></i>';
        button.title = 'تعديل';
        button.onclick = () => this.editItem(itemId, itemType);
        return button;
    }

    // إنشاء زر الحذف
    createDeleteButton(itemId, itemType) {
        const button = document.createElement('button');
        button.className = 'btn btn-sm btn-danger delete-btn';
        button.innerHTML = '<i class="fas fa-trash"></i>';
        button.title = 'حذف';
        button.onclick = () => this.deleteItem(itemId, itemType);
        return button;
    }

    // تعديل عنصر
    editItem(itemId, itemType) {
        if (!this.canEdit()) {
            this.showPermissionError('ليس لديك صلاحية للتعديل');
            return;
        }

        // إظهار نافذة التعديل حسب نوع العنصر
        switch(itemType) {
            case 'sticker':
                this.editSticker(itemId);
                break;
            case 'parking':
                this.editParking(itemId);
                break;
            case 'immobilized_car':
                this.editImmobilizedCar(itemId);
                break;
            case 'violation':
                this.editViolation(itemId);
                break;
            case 'incident':
                this.editIncident(itemId);
                break;
            case 'security_event':
                this.editSecurityEvent(itemId);
                break;
            case 'resident':
                this.editResident(itemId);
                break;
            case 'building':
                this.editBuilding(itemId);
                break;
            case 'apartment':
                this.editApartment(itemId);
                break;
            default:
                console.log('تعديل عنصر:', itemId, itemType);
        }
    }

    // حذف عنصر
    deleteItem(itemId, itemType) {
        if (!this.canDelete()) {
            this.showPermissionError('ليس لديك صلاحية للحذف');
            return;
        }

        // تأكيد الحذف
        if (confirm('هل أنت متأكد من حذف هذا العنصر؟ لا يمكن التراجع عن هذا الإجراء.')) {
            // تنفيذ الحذف حسب نوع العنصر
            switch(itemType) {
                case 'sticker':
                    this.deleteSticker(itemId);
                    break;
                case 'parking':
                    this.deleteParking(itemId);
                    break;
                case 'immobilized_car':
                    this.deleteImmobilizedCar(itemId);
                    break;
                case 'violation':
                    this.deleteViolation(itemId);
                    break;
                case 'incident':
                    this.deleteIncident(itemId);
                    break;
                case 'security_event':
                    this.deleteSecurityEvent(itemId);
                    break;
                case 'resident':
                    this.deleteResident(itemId);
                    break;
                case 'building':
                    this.deleteBuilding(itemId);
                    break;
                case 'apartment':
                    this.deleteApartment(itemId);
                    break;
                default:
                    console.log('حذف عنصر:', itemId, itemType);
            }
        }
    }

    // إظهار رسالة خطأ الصلاحيات
    showPermissionError(message) {
        alert(message || 'ليس لديك صلاحية لتنفيذ هذا الإجراء');
    }

    // دوال التعديل المخصصة لكل نوع
    editSticker(stickerId) {
        // إظهار نافذة تعديل الملصق
        this.showEditModal('sticker', stickerId);
    }

    editParking(parkingId) {
        // إظهار نافذة تعديل الموقف
        this.showEditModal('parking', parkingId);
    }

    editImmobilizedCar(carId) {
        // إظهار نافذة تعديل السيارة المكبوحة
        this.showEditModal('immobilized_car', carId);
    }

    editViolation(violationId) {
        // إظهار نافذة تعديل المخالفة
        this.showEditModal('violation', violationId);
    }

    editIncident(incidentId) {
        // إظهار نافذة تعديل الحادث
        this.showEditModal('incident', incidentId);
    }

    editSecurityEvent(eventId) {
        // إظهار نافذة تعديل الواقعة الأمنية
        this.showEditModal('security_event', eventId);
    }

    editResident(residentId) {
        // إظهار نافذة تعديل الساكن
        this.showEditModal('resident', residentId);
    }

    editBuilding(buildingId) {
        // إظهار نافذة تعديل المبنى
        this.showEditModal('building', buildingId);
    }

    editApartment(apartmentId) {
        // إظهار نافذة تعديل الشقة
        this.showEditModal('apartment', apartmentId);
    }

    // دوال الحذف المخصصة لكل نوع
    deleteSticker(stickerId) {
        console.log('حذف ملصق:', stickerId);
        // تنفيذ حذف الملصق
        this.performDelete('sticker', stickerId);
    }

    deleteParking(parkingId) {
        console.log('حذف موقف:', parkingId);
        // تنفيذ حذف الموقف
        this.performDelete('parking', parkingId);
    }

    deleteImmobilizedCar(carId) {
        console.log('حذف سيارة مكبوحة:', carId);
        // تنفيذ حذف السيارة المكبوحة
        this.performDelete('immobilized_car', carId);
    }

    deleteViolation(violationId) {
        console.log('حذف مخالفة:', violationId);
        // تنفيذ حذف المخالفة
        this.performDelete('violation', violationId);
    }

    deleteIncident(incidentId) {
        console.log('حذف حادث:', incidentId);
        // تنفيذ حذف الحادث
        this.performDelete('incident', incidentId);
    }

    deleteSecurityEvent(eventId) {
        console.log('حذف واقعة أمنية:', eventId);
        // تنفيذ حذف الواقعة الأمنية
        this.performDelete('security_event', eventId);
    }

    deleteResident(residentId) {
        console.log('حذف ساكن:', residentId);
        // تنفيذ حذف الساكن
        this.performDelete('resident', residentId);
    }

    deleteBuilding(buildingId) {
        console.log('حذف مبنى:', buildingId);
        // تنفيذ حذف المبنى
        this.performDelete('building', buildingId);
    }

    deleteApartment(apartmentId) {
        console.log('حذف شقة:', apartmentId);
        // تنفيذ حذف الشقة
        this.performDelete('apartment', apartmentId);
    }

    // إظهار نافذة التعديل
    showEditModal(itemType, itemId) {
        // إنشاء نافذة التعديل
        const modal = document.createElement('div');
        modal.className = 'edit-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>تعديل ${this.getItemTypeName(itemType)}</h3>
                    <button class="close-btn" onclick="this.parentElement.parentElement.parentElement.remove()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <p>نافذة تعديل ${this.getItemTypeName(itemType)} رقم: ${itemId}</p>
                    <p>سيتم تطوير هذه النافذة لاحقاً مع النماذج المناسبة</p>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-primary">حفظ التغييرات</button>
                    <button class="btn btn-secondary" onclick="this.parentElement.parentElement.parentElement.remove()">إلغاء</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
    }

    // تنفيذ الحذف
    performDelete(itemType, itemId) {
        // محاكاة حذف العنصر
        console.log(`تم حذف ${this.getItemTypeName(itemType)} رقم: ${itemId}`);
        
        // إزالة الصف من الجدول
        const row = document.querySelector(`[data-id="${itemId}"]`);
        if (row) {
            row.remove();
        }
        
        // إظهار رسالة نجاح
        this.showSuccessMessage(`تم حذف ${this.getItemTypeName(itemType)} بنجاح`);
    }

    // الحصول على اسم نوع العنصر
    getItemTypeName(itemType) {
        const names = {
            'sticker': 'الملصق',
            'parking': 'الموقف',
            'immobilized_car': 'السيارة المكبوحة',
            'violation': 'المخالفة',
            'incident': 'الحادث',
            'security_event': 'الواقعة الأمنية',
            'resident': 'الساكن',
            'building': 'المبنى',
            'apartment': 'الشقة'
        };
        return names[itemType] || 'العنصر';
    }

    // إظهار رسالة نجاح
    showSuccessMessage(message) {
        const alert = document.createElement('div');
        alert.className = 'alert alert-success';
        alert.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;
        alert.style.position = 'fixed';
        alert.style.top = '20px';
        alert.style.right = '20px';
        alert.style.zIndex = '9999';
        
        document.body.appendChild(alert);
        
        setTimeout(() => {
            alert.remove();
        }, 3000);
    }
}

// إنشاء مثيل من نظام الصلاحيات
const adminPermissions = new AdminPermissions();

// دوال مساعدة للاستخدام في الصفحات
function addEditDeleteToTable(tableId, itemType) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach((row, index) => {
        const itemId = row.dataset.id || index + 1;
        adminPermissions.addEditDeleteButtons(row, itemId, itemType);
    });
}

// إضافة أنماط CSS للنوافذ المنبثقة
const modalStyles = `
<style>
.edit-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10000;
}

.modal-content {
    background: white;
    border-radius: 10px;
    padding: 0;
    max-width: 500px;
    width: 90%;
    max-height: 80vh;
    overflow-y: auto;
}

.modal-header {
    background: #0f3d68;
    color: white;
    padding: 15px 20px;
    border-radius: 10px 10px 0 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-header h3 {
    margin: 0;
    font-size: 18px;
}

.close-btn {
    background: none;
    border: none;
    color: white;
    font-size: 18px;
    cursor: pointer;
    padding: 5px;
}

.modal-body {
    padding: 20px;
}

.modal-footer {
    padding: 15px 20px;
    border-top: 1px solid #eee;
    display: flex;
    gap: 10px;
    justify-content: flex-end;
}

.btn-sm {
    padding: 5px 10px;
    font-size: 12px;
    margin: 0 2px;
    border-radius: 4px;
    border: none;
    cursor: pointer;
}

.btn-warning {
    background: #ffc107;
    color: #000;
}

.btn-danger {
    background: #dc3545;
    color: white;
}

.btn-warning:hover {
    background: #e0a800;
}

.btn-danger:hover {
    background: #c82333;
}

.alert {
    padding: 12px 15px;
    border-radius: 5px;
    margin: 10px 0;
}

.alert-success {
    background: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}
</style>
`;

// إضافة الأنماط للصفحة
document.head.insertAdjacentHTML('beforeend', modalStyles);

