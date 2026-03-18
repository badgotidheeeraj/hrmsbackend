import re


class EmployeeLogic:
    def __init__(self, employee_model):
        self.employee_model = employee_model

    def _next_employee_id(self):
        last_employee = self.employee_model.objects.order_by('-id').first()
        if not last_employee or not last_employee.employee_id:
            return 'EMP001'

        match = re.search(r'(\d+)$', last_employee.employee_id)
        if not match:
            return 'EMP001'

        next_number = int(match.group(1)) + 1
        return f'EMP{next_number:03d}'

    def _resolve_employee(self, employee_identifier):
        try:
            if isinstance(employee_identifier, int) or str(employee_identifier).isdigit():
                return self.employee_model.objects.get(id=int(employee_identifier))

            return self.employee_model.objects.get(employee_id=employee_identifier)
        except self.employee_model.DoesNotExist:
            return None

    def create_employee(self, employee_data):
        # Auto-generate employee_id when not provided.
        if not employee_data.get('employee_id'):
            employee_data['employee_id'] = self._next_employee_id()

        employee = self.employee_model.objects.create(**employee_data)
        return employee

    def get_employee(self, employee_id):
        return self._resolve_employee(employee_id)

    def update_employee(self, employee_id, update_data):
        employee = self._resolve_employee(employee_id)
        if not employee:
            return None

        for key, value in update_data.items():
            setattr(employee, key, value)
        employee.save()
        return employee

    def delete_employee(self, employee_id):
        employee = self._resolve_employee(employee_id)
        if not employee:
            return False

        employee.delete()
        return True

    def mark_attendance(self, employee_id, date, status):
        from ..models import Attendance

        employee = self._resolve_employee(employee_id)
        if not employee:
            return None

        attendance, created = Attendance.objects.update_or_create(
            employee=employee,
            date=date,
            defaults={'status': status},
        )
        return attendance

    def get_attendance(self, employee_id, date=None):
        from ..models import Attendance

        employee = self._resolve_employee(employee_id)
        if not employee:
            return None

        if date:
            return Attendance.objects.filter(employee=employee, date=date)
        return Attendance.objects.filter(employee=employee)