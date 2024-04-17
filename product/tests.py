from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate

from .api.viewsets import ProductListAPIView, ProductCreateAPIView, ProductRetrieveAPIView, ProductUpdateAPIView, \
    ProductDestroyAPIView
from .models import Product, UNIT_TYPE_CHOICES


# Model tests
class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test', password='spw_2024', email='test@email.com')

    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            unit_type=1,
            created_by=self.user
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.description, 'Test Description')
        self.assertEqual(self.product.unit_type, 1)
        self.assertEqual(self.product.created_by, self.user)

    def test_unit_type_choices(self):
        choices = [choice[0] for choice in UNIT_TYPE_CHOICES]
        self.assertEqual(set(choices), set([choice[0] for choice in Product._meta.get_field('unit_type').choices]))


# Viewsets tests
class ProductViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='test', password='spw_2024', email='test@email.com',
                                             is_superuser=True)
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            unit_type=1,
            created_by=self.user
        )

    def test_product_list_authenticated(self):
        request = self.factory.get('/products/')
        force_authenticate(request, user=self.user)
        view = ProductListAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_product_list_unauthenticated(self):
        request = self.factory.get('/products/')
        view = ProductListAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 401)

    def test_product_create_authenticated(self):
        data = {
            'name': 'New Product',
            'description': 'New Description',
            'unit_type': 1
        }
        request = self.factory.post('/products/', data)
        force_authenticate(request, user=self.user)
        view = ProductCreateAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_product_create_unauthenticated(self):
        data = {
            'name': 'New Product',
            'description': 'New Description',
            'unit_type': 1
        }
        request = self.factory.post('/products/', data)
        view = ProductCreateAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 401)

    def test_product_retrieve_authenticated(self):
        request = self.factory.get(f'/products/{self.product.id}/')
        force_authenticate(request, user=self.user)
        view = ProductRetrieveAPIView.as_view()
        response = view(request, pk=self.product.id)
        self.assertEqual(response.status_code, 200)

    def test_product_retrieve_unauthenticated(self):
        request = self.factory.get(f'/products/{self.product.id}/')
        view = ProductRetrieveAPIView.as_view()
        response = view(request, pk=self.product.id)
        self.assertEqual(response.status_code, 401)

    def test_product_update_authenticated(self):
        data = {
            'name': 'Updated Product',
            'description': 'Updated Description',
            'unit_type': 1
        }
        request = self.factory.put(f'/products/{self.product.id}/', data)
        force_authenticate(request, user=self.user)
        view = ProductUpdateAPIView.as_view()
        response = view(request, pk=self.product.id)
        self.assertEqual(response.status_code, 200)

    def test_product_update_unauthenticated(self):
        data = {
            'name': 'Updated Product',
            'description': 'Updated Description',
            'unit_type': 1
        }
        request = self.factory.put(f'/products/{self.product.id}/', data)
        view = ProductUpdateAPIView.as_view()
        response = view(request, pk=self.product.id)
        self.assertEqual(response.status_code, 401)

    def test_product_destroy_authenticated(self):
        request = self.factory.delete(f'/products/{self.product.id}/')
        force_authenticate(request, user=self.user)
        view = ProductDestroyAPIView.as_view()
        response = view(request, pk=self.product.id)
        self.assertEqual(response.status_code, 204)

    def test_product_destroy_unauthenticated(self):
        request = self.factory.delete(f'/products/{self.product.id}/')
        view = ProductDestroyAPIView.as_view()
        response = view(request, pk=self.product.id)
        self.assertEqual(response.status_code, 401)
