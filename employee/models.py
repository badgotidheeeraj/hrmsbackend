from django.db import models


class Employee(models.Model):
    employee_id = models.CharField(max_length=36, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.employee_id:   # Only generate on create
            last_employee = Employee.objects.order_by('-id').first()

            if last_employee and last_employee.employee_id:
                last_number = int(last_employee.employee_id.replace("EMP", ""))
                new_number = last_number + 1
            else:
                new_number = 1

            self.employee_id = f"EMP{new_number:03d}"

        super().save(*args, **kwargs)




class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
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