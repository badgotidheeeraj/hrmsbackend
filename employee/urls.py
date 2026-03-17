from django.urls import path
from .views import EmployeeManagement, AttendanceManagement

urlpatterns = [
    path('employee-register/', EmployeeManagement.as_view()),
    path('employee-register/<int:employee_id>/', EmployeeManagement.as_view()),
    path('attendance/', AttendanceManagement.as_view()),
]