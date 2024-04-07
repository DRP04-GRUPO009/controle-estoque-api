from django.db import models
from product.models import Product
from school_unit.models import SchoolUnit
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Stock(models.Model):
    school_unit = models.OneToOneField(SchoolUnit, related_name='stock', on_delete=models.CASCADE, verbose_name='Unidade Escolar')

    class Meta:
        verbose_name='Estoque'
        verbose_name_plural='Estoques'

    def __str__(self):
        return f'Estoque - {self.school_unit}'

class StockItem(models.Model):
    stock = models.ForeignKey(Stock, related_name='items', on_delete=models.PROTECT, verbose_name='Estoque')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Produto')
    quantity = models.IntegerField(default=0, verbose_name='Quantidade')

    class Meta:
        verbose_name='Item do Estoque'
        verbose_name_plural='Itens do Estoque'

    def __str__(self):
        return f'{self.product}'
    
class StockTransfer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Produto')
    quantity = models.IntegerField(verbose_name='Quantidade')
    origin_school_unit = models.ForeignKey(SchoolUnit, related_name='origin_transfers', on_delete=models.PROTECT, verbose_name='Estoque de Origem')
    target_school_unit = models.ForeignKey(SchoolUnit, related_name='target_transfers', on_delete=models.PROTECT, verbose_name='Estoque de Destino')
    transfer_date = models.DateTimeField(auto_now=True, verbose_name='Data de Tranferência')
    transferred_by = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Transferido por')

    class Meta:
        verbose_name='Tranferência de Estoque'
        verbose_name_plural='Tranferências de Estoques'

    def perform_transfer(self):
        if self.quantity <= 0:
            raise ValidationError("A quantidade a ser transferida deve ser maior que zero.")

        if self.origin_school_unit == self.target_school_unit:
            raise ValidationError("A unidade de origem e a unidade de destino devem ser diferentes.")

        stock_item_origin = StockItem.objects.filter(stock__school_unit=self.origin_school_unit, product=self.product).first()
        if not stock_item_origin or stock_item_origin.quantity < self.quantity:
            raise ValidationError("A unidade de origem não possui quantidade suficiente do produto.")

        stock_item_origin.quantity -= self.quantity
        stock_item_origin.save()

        stock_item_target, created = StockItem.objects.get_or_create(stock=self.target_school_unit.stock, product=self.product)
            
        stock_item_target.quantity += self.quantity
        stock_item_target.save()

        self.save()
