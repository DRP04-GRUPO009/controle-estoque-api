from django.apps import AppConfig


class SchoolUnitConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'school_unit'

    def ready(self):
        import school_unit.signals