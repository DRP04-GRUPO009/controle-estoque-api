from django.urls import path
from product.api.viewsets import ProductCreateAPIView, ProductRetrieveAPIView, ProductUpdateAPIView, ProductDestroyAPIView, ProductListAPIView

urlpatterns = [
    path('', ProductListAPIView.as_view(), name='product-list'),
    path('novo/', ProductCreateAPIView.as_view(), name='product-create'),
    path('<int:pk>/', ProductRetrieveAPIView.as_view(), name='product-retrieve'),
    path('<int:pk>/alterar/', ProductUpdateAPIView.as_view(), name='product-update'),
    path('<int:pk>/excluir/', ProductDestroyAPIView.as_view(), name='product-delete'),
]
