from django.db import models
from django.contrib.auth.models import User

UNIT_TYPE_CHOICES = (
    (1, 'Unidade'),
    (2, 'Metro'),
    (3, 'Pacote'),
    (4, 'Bloco'),
    (5, 'Caixa'),
    (6, 'Rolo')
)


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nome')
    description = models.CharField(max_length=500, verbose_name='Descrição')
    unit_type = models.CharField(max_length=1, choices=UNIT_TYPE_CHOICES, verbose_name='Unidade de medida')
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Adicionado por')

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.name
