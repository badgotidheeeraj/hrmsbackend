import re


class EmployeeLogic:
    def __init__(self, employee_model):
        self.employee_model = employee_model

    def create_employee(self, employee_data):
        # Auto-generate employee_id when not provided.
        if not employee_data.get('employee_id'):
            employee_data['employee_id'] = self._next_employee_id()

        employee = self.employee_model.objects.create(**employee_data)
        return employee

    def get_employee(self, employee_id):
        return self._resolve_employee(employee_id)

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