# Generated by Django 5.0.2 on 2024-03-18 02:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0002_alter_product_created_at_alter_product_created_by_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_unit', models.CharField(max_length=150, verbose_name='Unidade Escolar')),
            ],
            options={
                'verbose_name': 'Estoque',
                'verbose_name_plural': 'Estoques',
            },
        ),
        migrations.CreateModel(
            name='StockItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='Quantidade')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.product', verbose_name='Produto')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='stock.stock', verbose_name='Estoque')),
            ],
            options={
                'verbose_name': 'Item do Estoque',
                'verbose_name_plural': 'Itens do Estoque',
            },
        ),
    ]