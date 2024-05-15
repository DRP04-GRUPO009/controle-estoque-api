from rest_framework import generics
from product.api import serializers
from controle_estoque_api.api.permissions import ApiProductPermissions, ReadOnlyUnlessStaff
from product import models
from product.helpers.filters import ProductFilter
from product.helpers.pagination import StandardPagination
from django_filters import rest_framework as filters


class ProductListAPIView(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    pagination_class = StandardPagination
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    permission_classes = [ReadOnlyUnlessStaff]


class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    permission_classes = [ApiProductPermissions]


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    permission_classes = [ApiProductPermissions]


class ProductUpdateAPIView(generics.UpdateAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    permission_classes = [ApiProductPermissions]


class ProductDestroyAPIView(generics.DestroyAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    permission_classes = [ApiProductPermissions]
