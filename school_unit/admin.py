from django.contrib import admin

from school_unit.models import SchoolUnit

@admin.register(SchoolUnit)
class SchoolUnitAdmin(admin.ModelAdmin):
    list_display = ['name']
