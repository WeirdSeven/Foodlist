from django.contrib import admin

# Register your models here.

from .models import Ingredient, Dish, Dish2Ingredient

class Dish2IngredientInline(admin.TabularInline):
	model = Dish2Ingredient
	extra = 1

class IngredientAdmin(admin.ModelAdmin):
	#inlines = (Dish2IngredientInline,)
	exclude = ('ratio', )
	

class DishAdmin(admin.ModelAdmin):
	inlines = (Dish2IngredientInline,)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Dish, DishAdmin)


admin.site.site_header = 'DeLaiQi 管理系统'
admin.site.site_title = 'My site admin'
admin.site.index_title = '站点管理'