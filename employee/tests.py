from rest_framework import status
from rest_framework.test import APITestCase


class WelcomeEndpointTests(APITestCase):
    def test_welcome_endpoint_returns_message(self):
        response = self.client.get('/api/welcome/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {'message': 'Welcome to the HRMS Backend API'}
        )


class EmployeeEmailUniquenessTests(APITestCase):
    def test_employee_email_must_be_unique(self):
        payload = {
            'full_name': 'Alice',
            'email': 'alice@example.com',
            'department': 'IT',
        }

        first_response = self.client.post('/api/employee-register/', payload, format='json')
        duplicate_response = self.client.post('/api/employee-register/', payload, format='json')

        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(duplicate_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', duplicate_response.json())
