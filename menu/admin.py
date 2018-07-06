from django.contrib import admin

# Register your models here.
from .models import Ingredient, Dish, Dish2Ingredient, Program, Program2Dish

class Dish2IngredientInline(admin.TabularInline):
	model = Dish2Ingredient
	extra = 1

class IngredientAdmin(admin.ModelAdmin):
	#inlines = (Dish2IngredientInline,)
	exclude = ('ratio', )
	
class DishAdmin(admin.ModelAdmin):
	inlines = (Dish2IngredientInline,)

class Program2DishInline(admin.TabularInline):
	model = Program2Dish
	extra = 1

class ProgramAdmin(admin.ModelAdmin):
	inlines = (Program2DishInline,)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(Program, ProgramAdmin)
