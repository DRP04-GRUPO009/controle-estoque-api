# Generated by Django 5.0.2 on 2024-04-07 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nome')),
                ('main_unit', models.BooleanField(default=False, verbose_name='Unidade Escolar Principal')),
            ],
            options={
                'verbose_name': 'Unidade Escolar',
                'verbose_name_plural': 'Unidades Escolares',
            },
        ),
    ]
