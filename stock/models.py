from django.db import models
from product.models import Product
from school_unit.models import SchoolUnit

class Stock(models.Model):
    school_unit = models.OneToOneField(SchoolUnit, related_name='stock', on_delete=models.PROTECT, verbose_name='Unidade Escolar')

    class Meta:
        verbose_name='Estoque'
        verbose_name_plural='Estoques'

    def __str__(self):
        return f'Estoque - {self.school_unit}'

class StockItem(models.Model):
    stock = models.ForeignKey(Stock, related_name='items', on_delete=models.CASCADE, verbose_name='Estoque')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Produto')
    quantity = models.IntegerField(verbose_name='Quantidade')

    class Meta:
        verbose_name='Item do Estoque'
        verbose_name_plural='Itens do Estoque'

    def __str__(self):
        return f'{self.product}'
