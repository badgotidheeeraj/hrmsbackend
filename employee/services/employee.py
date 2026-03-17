




class EmployeeLogic:
    def __init__(self, employee_model):
        self.employee_model = employee_model

    def create_employee(self, employee_data):
        # Logic to create an employee
        employee = self.employee_model.objects.create(**employee_data)
        return employee

    def get_employee(self, employee_id):
        # Logic to retrieve an employee by ID
        try:
            return self.employee_model.objects.get(id=employee_id)
        except self.employee_model.DoesNotExist:
            return None

    def update_employee(self, employee_id, update_data):
        # Logic to update an existing employee
        try:
            employee = self.employee_model.objects.get(id=employee_id)
            for key, value in update_data.items():
                setattr(employee, key, value)
            employee.save()
            return employee
        except self.employee_model.DoesNotExist:
            return None

    def delete_employee(self, employee_id):
        # Logic to delete an employee
        try:
            employee = self.employee_model.objects.get(id=employee_id)
            employee.delete()
            return True
        except self.employee_model.DoesNotExist:
            return False

    def mark_attendance(self, employee_id, date, status):
        from ..models import Attendance

        try:
            employee = self.employee_model.objects.get(id=employee_id)
        except self.employee_model.DoesNotExist:
            return None

        attendance, created = Attendance.objects.update_or_create(
            employee=employee,
            date=date,
            defaults={'status': status},
        )
        return attendance

    def get_attendance(self, employee_id, date=None):
        from ..models import Attendance

        try:
            employee = self.employee_model.objects.get(id=employee_id)
        except self.employee_model.DoesNotExist:
            return None

        if date:
            return Attendance.objects.filter(employee=employee, date=date)
        return Attendance.objects.filter(employee=employee)
