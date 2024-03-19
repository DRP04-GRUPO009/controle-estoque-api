from django.db.models.signals import post_save
from django.dispatch import receiver

from school_unit.models import SchoolUnit
from stock.models import Stock

@receiver(post_save, sender=SchoolUnit)
def create_stock_for_school_unit(sender, instance, created, **kwargs):
    if created:
        Stock.objects.create(school_unit=instance)
        