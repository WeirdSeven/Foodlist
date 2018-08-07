from django.contrib import admin

# Register your models here.
from .models import *

class IngredientAdmin(admin.ModelAdmin):
	#inlines = (Dish2IngredientInline,)
	exclude = ('ratio', )
	ordering = ['name']
	search_fields = ['name']

class Dish2IngredientInline(admin.TabularInline):
	model = Dish2Ingredient
	autocomplete_fields = ['ingredient']
	extra = 1
	
class DishAdmin(admin.ModelAdmin):
	inlines = [Dish2IngredientInline]
	search_fields = ['name']

class Program2DishInline(admin.TabularInline):
	model = Program2Dish
	autocomplete_fields = ['dish']
	extra = 1

class CongeeSoup2IngredientInline(admin.TabularInline):
	model = CongeeSoup2Ingredient
	autocomplete_fields = ['ingredient']
	extra = 1

class CongeeSoupAdmin(admin.ModelAdmin):
	inlines = [CongeeSoup2IngredientInline]
	search_fields = ['name']

class Program2CongeeSoupInline(admin.TabularInline):
	model = Program2CongeeSoup
	autocomplete_fields = ['congeesoup']
	extra = 1

class StapleAdmin(admin.ModelAdmin):
	search_fields = ['name']

class Program2StapleInline(admin.TabularInline):
	model = Program2Staple
	autocomplete_fields = ['staple']
	extra = 1

class OilAdmin(admin.ModelAdmin):
	search_fields = ['name']

class Program2OilInline(admin.TabularInline):
	model = Program2Oil
	autocomplete_fields = ['oil']
	extra = 1

class DisposableAdmin(admin.ModelAdmin):
	search_fields = ['name']

class Program2DisposableInline(admin.TabularInline):
	model = Program2Disposable
	autocomplete_fields = ['disposable']
	extra = 1

class ProgramAdmin(admin.ModelAdmin):
	inlines = [
		Program2DishInline, 
		Program2CongeeSoupInline, 
		Program2StapleInline,
		Program2OilInline, 
		Program2DisposableInline,
	]

class SuperProgramAdmin(admin.ModelAdmin):
	pass

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(CongeeSoup, CongeeSoupAdmin)
admin.site.register(Staple, StapleAdmin)
admin.site.register(Oil, OilAdmin)
admin.site.register(Disposable, DisposableAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(SuperProgram, SuperProgramAdmin)
