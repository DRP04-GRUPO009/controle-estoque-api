from django.db import models


class SchoolUnit(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nome')
    main_unit = models.BooleanField(default=False, verbose_name='Unidade Escolar Principal')

    class Meta:
        verbose_name = 'Unidade Escolar'
        verbose_name_plural = 'Unidades Escolares'

    def save(self, *args, **kwargs):
        if self.main_unit:
            SchoolUnit.objects.exclude(pk=self.pk).update(main_unit=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
