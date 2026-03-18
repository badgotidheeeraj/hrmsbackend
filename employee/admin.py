from django.contrib import admin
from .models import Employee, Attendance

# Register your models here.


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in_time')
    search_fields = ('employee__full_name', 'date')
    list_filter = ('date', 'employee')
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'full_name', 'email', 'department', 'created_at')
    search_fields = ('employee_id', 'full_name', 'email', 'department')
    list_filter = ('department', 'created_at')