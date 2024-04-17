from django.contrib.auth.models import User
from django.test import TestCase

from user.api.serializers import CustomTokenObtainPairSerializer


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='spw_2024', email='test@email.com')

    def test_login(self):
        self.assertTrue(self.user.is_authenticated)

        serializer = CustomTokenObtainPairSerializer()
        token = serializer.get_token(self.user)
        self.assertEqual(token['username'], self.user.username)
        self.assertEqual(token['is_staff'], self.user.is_staff)
