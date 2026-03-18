from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Employee, Attendance


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'employee_id', 'full_name', 'email', 'department', 'created_at', 'updated_at']
        read_only_fields = ['id', 'employee_id', 'created_at', 'updated_at']


class AttendanceSerializer(serializers.ModelSerializer):
    employee_code = serializers.CharField(source='employee.employee_id', read_only=True)
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id',
            'employee',
            'employee_code',
            'employee_name',
            'date',
            'status',
            'check_in_time',
            'check_out_time',
        ]
        read_only_fields = ['id', 'employee_code', 'employee_name']
        validators = [
            UniqueTogetherValidator(
                queryset=Attendance.objects.all(),
                fields=['employee', 'date'],
                message='Attendance is already present for this employee on this date.',
            )
        ]
