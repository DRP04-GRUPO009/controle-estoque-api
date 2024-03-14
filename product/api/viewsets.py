from rest_framework import generics
from product.api import serializers
from product.api.permissions import ReadOnlyUnlessStaff
from product import models

class ProductListAPIView(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    permission_classes = [ReadOnlyUnlessStaff]

class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    permission_classes = [ReadOnlyUnlessStaff]

class ProductRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    permission_classes = [ReadOnlyUnlessStaff]

class ProductUpdateAPIView(generics.UpdateAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    permission_classes = [ReadOnlyUnlessStaff]

class ProductDestroyAPIView(generics.DestroyAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    permission_classes = [ReadOnlyUnlessStaff]
