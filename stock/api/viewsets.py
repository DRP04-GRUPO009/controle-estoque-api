from django.db import transaction
from django.forms import ValidationError
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from controle_estoque_api.api.permissions import ApiStockItemPermissions
from stock.api.serializers import StockItemWriteSerializer, StockTransferWriteSerializer
from stock.models import StockItem, StockTransfer


# StockItem
class StockItemCreateAPIView(generics.CreateAPIView):
    serializer_class = StockItemWriteSerializer
    queryset = StockItem.objects.all()
    permission_classes = [ApiStockItemPermissions]


class StockItemUpdateApiView(generics.UpdateAPIView):
    serializer_class = StockItemWriteSerializer
    queryset = StockItem.objects.all()
    permission_classes = [ApiStockItemPermissions]


class StockItemDeleteApiView(generics.DestroyAPIView):
    serializer_class = StockItemWriteSerializer
    queryset = StockItem.objects.all()
    permission_classes = [ApiStockItemPermissions]


# StockTransfer
class StockTransferCreateAPIView(viewsets.ModelViewSet):
    serializer_class = StockTransferWriteSerializer
    queryset = StockTransfer.objects.all()
    permission_classes = [ApiStockItemPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        product = data['product']
        quantity = data['quantity']
        origin_school_unit = data['origin_school_unit']
        target_school_unit = data['target_school_unit']
        transferred_by = request.user

        try:
            with transaction.atomic():
                transfer = StockTransfer.objects.create(
                    product=product,
                    quantity=quantity,
                    origin_school_unit=origin_school_unit,
                    target_school_unit=target_school_unit,
                    transferred_by=transferred_by
                )

                transfer.perform_transfer()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error:": str(e)}, status=status.HTTP_400_BAD_REQUEST)
