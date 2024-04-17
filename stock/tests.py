from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.test import force_authenticate, APIRequestFactory

from product.api.viewsets import ProductDestroyAPIView, ProductUpdateAPIView, ProductRetrieveAPIView, \
    ProductCreateAPIView, ProductListAPIView
from .models import Stock, StockItem, StockTransfer
from product.models import Product
from school_unit.models import SchoolUnit
from django.core.exceptions import ValidationError

# Models unit tests


class StockTestCase(TestCase):
    def setUp(self):
        self.school_unit = SchoolUnit.objects.create(name='School Unit 1')
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_stock_creation(self):
        stock = self.school_unit.stock  # O estoque deve ser criado automaticamente ao criar uma SchoolUnit
        self.assertIsNotNone(stock)
        self.assertEqual(stock.school_unit, self.school_unit)


class StockItemTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='spw_2024', email='test@email.com')
        self.school_unit = SchoolUnit.objects.create(name='School Unit 1')
        self.product = Product.objects.create(name='Product 1', description='Description 1', unit_type='1', created_by=self.user)

    def test_stock_item_creation(self):
        stock = self.school_unit.stock
        stock_item = StockItem.objects.create(stock=stock, product=self.product, quantity=10)
        self.assertEqual(stock_item.stock, stock)
        self.assertEqual(stock_item.product, self.product)
        self.assertEqual(stock_item.quantity, 10)


class StockTransferTestCase(TestCase):
    def setUp(self):
        self.origin_school_unit = SchoolUnit.objects.create(name='Origin School Unit')
        self.target_school_unit = SchoolUnit.objects.create(name='Target School Unit')
        self.user = User.objects.create_user(username='test', password='spw_2024', email='test@email.com')
        self.product = Product.objects.create(name='Product 1', description='Description 1', unit_type='1',  created_by=self.user)

    def test_stock_transfer(self):
        stock_origin = self.origin_school_unit.stock
        stock_target = self.target_school_unit.stock
        stock_item_origin = StockItem.objects.create(stock=stock_origin, product=self.product, quantity=20)
        transfer = StockTransfer.objects.create(product=self.product, quantity=10,
                                                origin_school_unit=self.origin_school_unit,
                                                target_school_unit=self.target_school_unit, transferred_by=self.user)
        transfer.perform_transfer()

        # Testar se a quantidade foi transferida corretamente
        stock_item_origin.refresh_from_db()
        self.assertEqual(stock_item_origin.quantity, 10)

        stock_item_target = StockItem.objects.get(stock=stock_target, product=self.product)
        self.assertEqual(stock_item_target.quantity, 10)

    def test_invalid_transfer(self):
        with self.assertRaises(ValidationError):
            # Tenta transferir uma quantidade maior do que a disponível
            stock_origin = self.origin_school_unit.stock
            stock_target = self.target_school_unit.stock
            stock_item_origin = StockItem.objects.create(stock=stock_origin, product=self.product, quantity=20)
            transfer = StockTransfer.objects.create(product=self.product, quantity=30,
                                                    origin_school_unit=self.origin_school_unit,
                                                    target_school_unit=self.target_school_unit,
                                                    transferred_by=self.user)
            transfer.perform_transfer()

        with self.assertRaises(ValidationError):
            # Tenta transferir para a mesma unidade de origem e destino
            transfer = StockTransfer.objects.create(product=self.product, quantity=10,
                                                    origin_school_unit=self.origin_school_unit,
                                                    target_school_unit=self.origin_school_unit,
                                                    transferred_by=self.user)
            transfer.perform_transfer()

        with self.assertRaises(ValidationError):
            # Tenta transferir uma quantidade negativa
            transfer = StockTransfer.objects.create(product=self.product, quantity=-10,
                                                    origin_school_unit=self.origin_school_unit,
                                                    target_school_unit=self.target_school_unit,
                                                    transferred_by=self.user)
            transfer.perform_transfer()


# Viewsets unit tests


class ProductListViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='test', password='spw_2024', email='test@email.com')
        self.staff_user = User.objects.create_user(username='staffuser', password='testpassword', is_staff=True)
        self.group = Group.objects.create(name='Group 1')
        self.user.groups.add(self.group)
        self.product = Product.objects.create(name='Product 1', description='Description 1', unit_type='1', created_by=self.user)

    def test_product_list_authenticated(self):
        view = ProductListAPIView.as_view()
        request = self.factory.get('/products/')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_list_unauthenticated(self):
        view = ProductListAPIView.as_view()
        request = self.factory.get('/products/')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_list_staff_authenticated(self):
        view = ProductListAPIView.as_view()
        request = self.factory.get('/products/')
        force_authenticate(request, user=self.staff_user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductCreateViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='test', password='spw_2024', email='test@email.com')

    def test_product_create_authenticated(self):
        view = ProductCreateAPIView.as_view()
        request = self.factory.post('/products/', {'name': 'Product 1', 'description': 'Description 1', 'unit_type': '1', 'created_by': self.user})
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_product_create_unauthenticated(self):
        view = ProductCreateAPIView.as_view()
        request = self.factory.post('/products/', {'name': 'Product 1', 'description': 'Description 1', 'unit_type': '1', 'created_by': self.user})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProductRetrieveViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='test', password='spw_2024', email='test@email.com')
        self.product = Product.objects.create(name='Product 1', description='Description 1', unit_type='1', created_by=self.user)

    def test_product_retrieve_authenticated(self):
        view = ProductRetrieveAPIView.as_view()
        request = self.factory.get('/products/1/')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.product.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_retrieve_unauthenticated(self):
        view = ProductRetrieveAPIView.as_view()
        request = self.factory.get('/products/1/')
        response = view(request, pk=self.product.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProductUpdateViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='test', password='spw_2024', email='test@email.com')
        self.product = Product.objects.create(name='Product 1', description='Description 1', unit_type='1', created_by=self.user)

    def test_product_update_authenticated(self):
        view = ProductUpdateAPIView.as_view()
        request = self.factory.put('/products/1/', {'name': 'Updated Product', 'description': 'Updated Description', 'unit_type': '2', 'created_by': self.user})
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.product.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_update_unauthenticated(self):
        view = ProductUpdateAPIView.as_view()
        request = self.factory.put('/products/1/', {'name': 'Updated Product', 'description': 'Updated Description', 'unit_type': '2', 'created_by': self.user})
        response = view(request, pk=self.product.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProductDestroyViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='test', password='spw_2024', email='test@email.com')
        self.product = Product.objects.create(name='Product 1', description='Description 1', unit_type='1', created_by=self.user)

    def test_product_destroy_authenticated(self):
        view = ProductDestroyAPIView.as_view()
        request = self.factory.delete('/products/1/')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.product.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_product_destroy_unauthenticated(self):
        view = ProductDestroyAPIView.as_view()
        request = self.factory.delete('/products/1/')
        response = view(request, pk=self.product.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
