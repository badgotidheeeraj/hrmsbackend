from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Employee, Attendance
from .serializers import EmployeeSerializer, AttendanceSerializer
from .services.employee import EmployeeLogic


class WelcomeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "message": "Welcome to the HRMS Backend API"
        }, status=status.HTTP_200_OK)


class EmployeeManagement(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.employee_logic = EmployeeLogic(Employee)

    # Create Employee
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        employee = self.employee_logic.create_employee(serializer.validated_data)

        return Response(EmployeeSerializer(employee).data, status=201)

    # Get Employee / List Employees
    def get(self, request, employee_id=None):
        if employee_id:
            employee = self.employee_logic.get_employee(employee_id)
            if not employee:
                return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

            data = EmployeeSerializer(employee).data
            return Response(data)

        employees = Employee.objects.all()
        data = EmployeeSerializer(employees, many=True).data
        return Response(data)

 

    # Delete Employee
    def delete(self, request, employee_id):
        deleted = self.employee_logic.delete_employee(employee_id)
        if not deleted:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Employee deleted"}, status=status.HTTP_204_NO_CONTENT)



class AttendanceManagement(APIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.employee_logic = EmployeeLogic(Employee)

    def post(self, request):
        request_data = request.data
        employee_identifier = request_data.get('employee_id') or request_data.get('employee')
        date = request_data.get('date')
        status_value = request_data.get('status')

        if not employee_identifier or not date or not status_value:
            return Response({
                'error': 'employee (or employee_id), date and status are required fields.'
            }, status=status.HTTP_400_BAD_REQUEST)

        normalized_status = str(status_value).strip().lower()
        status_map = {
            'present': 'Present',
            'absent': 'Absent',
            'leave': 'On Leave',
            'on leave': 'On Leave',
        }
        status_value = status_map.get(normalized_status)

        # Validate status is allowed
        if not status_value:
            return Response({
                'error': 'status must be Present, Absent or On Leave.'
            }, status=status.HTTP_400_BAD_REQUEST)

        employee = self.employee_logic.get_employee(employee_identifier)
        if not employee:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        serialized = AttendanceSerializer(data={
            'employee': employee.id,
            'date': date,
            'status': status_value,
        })

        if not serialized.is_valid():
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        attendance = self.employee_logic.mark_attendance(employee.id, date, status_value)
        if attendance is None:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        output = AttendanceSerializer(attendance)
        return Response(output.data, status=status.HTTP_201_CREATED)

    def get(self, request, employee_id=None):
        employee_id = employee_id or request.query_params.get('employee_id') or request.query_params.get('employee')
        date = request.query_params.get('date')

        # List all attendance records when employee_id is not provided.
        if not employee_id:
            serialized = AttendanceSerializer(Attendance.objects.all(), many=True)
            return Response(serialized.data)

        attendances = self.employee_logic.get_attendance(employee_id, date)
        if attendances is None:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        serialized = AttendanceSerializer(attendances, many=True)
        return Response(serialized.data)
