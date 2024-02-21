# from django.test import TestCase

# Create your tests here.

from django.test import TestCase


class TestApp(TestCase):
    def test_app(self) -> None:
        self.assertTrue(True)

    def test_app2(self) -> None:
        response = self.client.get('/')
        assert response.status_code == 404
