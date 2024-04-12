from django.contrib.auth.models import Group
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from school_unit.models import SchoolUnit
from stock.models import Stock


@receiver(post_save, sender=SchoolUnit)
def create_stock_for_school_unit(sender, instance, created, **kwargs):
    if created:
        Stock.objects.create(school_unit=instance)


@receiver(post_save, sender=SchoolUnit)
def create_group_for_school_unit(sender, instance, created, **kwargs):
    if created:
        group_name = f'Grupo_{instance.name}'
        group_pk = instance.pk
        Group.objects.create(name=group_name, pk=group_pk)
        
        
@receiver(pre_save, sender=SchoolUnit)
def update_group_for_school_unit(sender, instance, **kwargs):
    if instance.pk: 
        old_group_name = f"Grupo_{SchoolUnit.objects.get(pk=instance.pk).name}"
        new_group_name = f"Grupo_{instance.name}"
        if old_group_name != new_group_name:
            try:
                group = Group.objects.get(name=old_group_name)
                print(group)
                group.name = new_group_name
                group.save()
            except Group.DoesNotExist:
                pass



