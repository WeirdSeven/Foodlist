from django.apps import AppConfig


class CommonConfig(AppConfig):
    admin_priority = 11
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'
    verbose_name = '通用'
