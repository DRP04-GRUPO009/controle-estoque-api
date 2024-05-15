from django_filters import rest_framework as filters
from product.models import Product


class ProductFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('created_at', 'created_at'),
        ),
        field_labels={
            'name': 'Nome',
            'created_at': 'Data de Cadastro',
        },
        label='Ordenação',
    )

    class Meta:
        model = Product
        fields = []
