from django.apps import AppConfig


class AccountsConfig(AppConfig):
    admin_priority = 1
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = ' 账户'
