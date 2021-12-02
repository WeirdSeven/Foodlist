from django.apps import AppConfig


class PurchasingConfig(AppConfig):
    admin_priority = 20
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'purchasing'
    verbose_name = '采购'
