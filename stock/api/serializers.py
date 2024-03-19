from rest_framework import serializers
from product.api.serializers import ProductSerializer
from stock.models import StockItem, Stock

class StockItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = StockItem
        fields = '__all__'

class StockItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockItem
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    items = StockItemSerializer(many=True)

    class Meta:
        model = Stock
        fields = '__all__'
