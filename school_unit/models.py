from django.db import models

class SchoolUnit(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nome')

    class Meta:
        verbose_name='Unidade Escolar'
        verbose_name_plural='Unidades Escolares'
        
    def __str__(self):
        return self.name