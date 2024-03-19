from rest_framework import generics
from controle_estoque_api.api.permissions import ReadOnlyUnlessStaff
from stock.api.serializers import StockItemWriteSerializer
from stock.models import StockItem

class StockItemCreateAPIView(generics.CreateAPIView):
    serializer_class = StockItemWriteSerializer
    queryset = StockItem.objects.all()
    permission_classes = [ReadOnlyUnlessStaff]

class StockItemUpdateApiView(generics.UpdateAPIView):
    serializer_class = StockItemWriteSerializer
    queryset = StockItem.objects.all()
    permission_classes = [ReadOnlyUnlessStaff]

class StockItemDeleteApiView(generics.DestroyAPIView):
    serializer_class = StockItemWriteSerializer
    queryset = StockItem.objects.all()
    permission_classes = [ReadOnlyUnlessStaff]
