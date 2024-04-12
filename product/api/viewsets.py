from rest_framework import generics
from product.api import serializers
from controle_estoque_api.api.permissions import ApiProductPermissions, ReadOnlyUnlessStaff
from product import models


class ProductListAPIView(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
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
