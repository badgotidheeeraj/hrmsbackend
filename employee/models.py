from django.db import models


class Employee(models.Model):
    employee_id = models.CharField(max_length=36, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def create_employee(self, validated_data):
        last_employee = Employee.objects.order_by('-id').first()

        if last_employee:
            last_id = int(last_employee.empid.replace('EMP', ''))
            new_id = f"EMP{last_id + 1:03d}"
        else:
            new_id = "EMP001"

        validated_data["empid"] = new_id

        employee = Employee.objects.create(**validated_data)
        return employee




class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('On Leave', 'On Leave'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"Attendance for {self.employee.full_name} on {self.date} ({self.status})"   
