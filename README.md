# HRMS Backend

A Django + Django REST Framework backend for employee management and attendance tracking.

## Tech Stack

- Python 3
- Django 6.0.3
- Django REST Framework 3.16.1
- django-cors-headers 4.9.0
- SQLite (default)

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run migrations:

```bash
python manage.py migrate
```

4. Start development server:

```bash
python manage.py runserver
```

Base URL: `http://127.0.0.1:8000`

## API Endpoints

All endpoints are prefixed with `/api/`.

### Welcome

- `GET /api/welcome/` - Simple welcome message to confirm the API is running

### Employees

- `POST /api/employee-register/` - Create employee (employee code is auto-generated, e.g. `EMP001`)
- `GET /api/employee-register/` - List all employees
- `GET /api/employee-register/<employee_id>/` - Get one employee
- `DELETE /api/employee-register/<employee_id>/` - Delete employee

Create employee example:

```json
{
  "full_name": "Dheeraj",
  "email": "dheeraj@example.com",
  "department": "IT"
}
```

### Attendance

- `POST /api/attendance/` - Mark attendance
- `GET /api/attendance/` - List all attendance records
- `GET /api/attendance/<employee_id>/` - Attendance for one employee
- `GET /api/attendance/?employee_id=EMP001` - Attendance by query param
- `GET /api/attendance/?employee=EMP001` - Alternate query param

Mark attendance example:

```json
{
  "employee": "EMP001",
  "date": "2026-03-18",
  "status": "leave"
}
```

Accepted status values:

- `present`
- `absent`
- `leave`

They are normalized and stored as:

- `Present`
- `Absent`
- `On Leave`

## Notes

- Duplicate attendance for the same employee and date is blocked.
- API returns a clear message when attendance already exists for that date.
