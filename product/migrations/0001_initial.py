# Generated by Django 5.0.2 on 2024-04-07 17:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Nome')),
                ('description', models.CharField(max_length=500, verbose_name='Descrição')),
                ('unit_type', models.CharField(choices=[(1, 'Unidade'), (2, 'Metro'), (3, 'Pacote'), (4, 'Bloco'), (5, 'Caixa'), (6, 'Rolo')], max_length=1, verbose_name='Unidade de medida')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Adicionado por')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
            },
        ),
    ]
