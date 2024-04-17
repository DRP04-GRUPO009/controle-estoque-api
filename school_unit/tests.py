from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from controle_estoque_api.api.permissions import ApiSchoolUnitPermissions
from .api.viewsets import SchoolUnitListAPIView, SchoolUnitRetrieveApiView, SchoolUnitCreateApiView, \
    SchoolUnitUpdateApiView, SchoolUnitDestroyApiView
from .models import SchoolUnit


# Model unit tests
class SchoolUnitModelTest(TestCase):
    def test_school_unit_creation(self):
        unit = SchoolUnit.objects.create(name='Test School Unit', main_unit=True)

        self.assertEqual(unit.name, 'Test School Unit')
        self.assertTrue(unit.main_unit)

    def test_main_unit_update(self):
        unit1 = SchoolUnit.objects.create(name='Main Unit', main_unit=True)
        unit2 = SchoolUnit.objects.create(name='Secondary Unit', main_unit=False)

        # Atualiza a segunda unidade para ser a principal
        unit2.main_unit = True
        unit2.save()

        # Verifica se apenas uma unidade é marcada como principal
        self.assertTrue(SchoolUnit.objects.filter(main_unit=True).count() == 1)
        self.assertEqual(SchoolUnit.objects.get(main_unit=True), unit2)


# Viewsets unit tests
class MockRequest:
    def __init__(self, user=None, query_params=None):
        self.user = user
        self.query_params = query_params


class SchoolUnitViewSetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        cls.user = User.objects.create_user(username='test', password='spw_2024', email='test@email.com')

    def setUp(self):
        self.unit = SchoolUnit.objects.create(name='Test Unit', main_unit=True)

    def test_school_unit_list_authenticated(self):
        request = self.factory.get('/school_units/')
        force_authenticate(request, user=self.user)
        view = SchoolUnitListAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_school_unit_list_unauthenticated(self):
        request = self.factory.get('/school_units/')
        view = SchoolUnitListAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_school_unit_retrieve_authenticated(self):
        url = reverse('school-unit-retrieve', kwargs={'pk': self.unit.pk})
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        view = SchoolUnitRetrieveApiView.as_view()
        response = view(request, pk=self.unit.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_school_unit_retrieve_unauthenticated(self):
        url = reverse('school-unit-retrieve', kwargs={'pk': self.unit.pk})
        request = self.factory.get(url)
        view = SchoolUnitRetrieveApiView.as_view()
        response = view(request, pk=self.unit.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_school_unit_create_authenticated(self):
        url = '/school_units/'
        data = {
            'name': 'New Unit',
            'main_unit': False
        }
        request = self.factory.post(url, data)
        force_authenticate(request, user=self.user)
        view = SchoolUnitCreateApiView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_school_unit_create_unauthenticated(self):
        url = '/school_units/'
        data = {
            'name': 'New Unit',
            'main_unit': False
        }
        request = self.factory.post(url, data)
        view = SchoolUnitCreateApiView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_school_unit_update_authenticated(self):
        url = reverse('school-unit-update', kwargs={'pk': self.unit.pk})
        data = {
            'name': 'Updated Unit',
            'main_unit': False
        }
        request = self.factory.put(url, data)
        force_authenticate(request, user=self.user)
        view = SchoolUnitUpdateApiView.as_view()
        response = view(request, pk=self.unit.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_school_unit_update_unauthenticated(self):
        url = reverse('school-unit-update', kwargs={'pk': self.unit.pk})
        data = {
            'name': 'Updated Unit',
            'main_unit': False
        }
        request = self.factory.put(url, data)
        view = SchoolUnitUpdateApiView.as_view()
        response = view(request, pk=self.unit.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_school_unit_destroy_authenticated(self):
        url = reverse('school-unit-delete', kwargs={'pk': self.unit.pk})
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)
        view = SchoolUnitDestroyApiView.as_view()
        response = view(request, pk=self.unit.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_school_unit_destroy_unauthenticated(self):
        url = reverse('school-unit-delete', kwargs={'pk': self.unit.pk})
        request = self.factory.delete(url)
        view = SchoolUnitDestroyApiView.as_view()
        response = view(request, pk=self.unit.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ApiSchoolUnitPermissionsTest(TestCase):
    def setUp(self):
        self.permission = ApiSchoolUnitPermissions()
        self.user = User.objects.create_user(username='test1', password='spw_2024', email='test1@email.com')
        self.staff_user = User.objects.create_user(username='test2', password='spw_2024', email='test2@email.com', is_staff=True)
        self.unit = SchoolUnit.objects.create(name='Test Unit', main_unit=True)

        self.group = Group.objects.get(name=f'Grupo_{self.unit.name}')

        # Adicionar o usuário ao grupo
        self.group.user_set.add(self.user)

    def test_has_permission_authenticated_staff(self):
        request = MockRequest(user=self.staff_user)
        self.assertTrue(self.permission.has_permission(request, None))

    def test_has_permission_authenticated_no_groups(self):
        request = MockRequest(user=self.user)
        request.user.groups.clear()
        self.assertTrue(self.permission.has_permission(request, None))

    def test_has_permission_authenticated_with_groups(self):
        request = MockRequest(user=self.user, query_params={'pk': self.unit.pk})
        self.assertTrue(self.permission.has_permission(request, None))

    def test_has_permission_authenticated_wrong_group(self):
        self.user.groups.clear()
        wrong_group = Group.objects.create(name='Wrong Group')
        wrong_group.user_set.add(self.user)
        request = MockRequest(user=self.user, query_params={'pk': self.unit.pk})
        self.assertFalse(self.permission.has_permission(request, None))

    def test_has_permission_unauthenticated(self):
        request = MockRequest()
        self.assertFalse(self.permission.has_permission(request, None))

