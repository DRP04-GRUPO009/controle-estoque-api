# Generated by Django 5.0.2 on 2024-04-07 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockitem',
            name='quantity',
            field=models.IntegerField(null=True, verbose_name='Quantidade'),
        ),
    ]
