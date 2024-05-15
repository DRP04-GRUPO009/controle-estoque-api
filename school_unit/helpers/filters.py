from django_filters import rest_framework as filters
from ..models import SchoolUnit


class SchoolUnitFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('name', 'name'),
        ),
        field_labels={
            'name': 'Nome',
        },
        label='Ordenação',
    )

    class Meta:
        model = SchoolUnit
        fields = []
