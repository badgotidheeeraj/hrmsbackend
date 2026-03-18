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
