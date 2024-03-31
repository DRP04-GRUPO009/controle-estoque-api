from django.urls import path
from stock.api.viewsets import StockItemCreateAPIView, StockItemUpdateApiView, StockItemDeleteApiView, StockTransferCreateAPIView

urlpatterns = [
    path('item-estoque/novo/', StockItemCreateAPIView.as_view(), name='new-stock-item'),
    path('item-estoque/<int:pk>/alterar/', StockItemUpdateApiView.as_view(), name='update-stock-item'),
    path('item-estoque/<int:pk>/excluir/', StockItemDeleteApiView.as_view(), name='delete-stock-item'),
    path('item-estoque/transferir/', StockTransferCreateAPIView.as_view({'post': 'create'}), name='transfer-stock-item')
]
