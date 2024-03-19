from rest_framework import serializers
from school_unit.models import SchoolUnit
from stock.api.serializers import StockSerializer

class SchoolUnitSerializer(serializers.ModelSerializer):
    stock = StockSerializer()

    class Meta:
        model = SchoolUnit
        fields = ['name', 'stock']