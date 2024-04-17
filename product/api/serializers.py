from rest_framework import serializers
from product import models


class ProductSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Product
        fields = '__all__'
