from __future__ import unicode_literals

from django.apps import AppConfig


class MenuConfig(AppConfig):
	admin_priority = 15
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'menu'
	verbose_name = '配菜系统'
