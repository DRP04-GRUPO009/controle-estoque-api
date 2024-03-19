from rest_framework import serializers
from stock.models import StockItem, Stock

class StockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockItem
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    items = StockItemSerializer(many=True)

    class Meta:
        model = Stock
        fields = '__all__'
