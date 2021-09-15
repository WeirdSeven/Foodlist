from django.contrib import admin

# Register your models here.
from .models import *
from django.forms import *
import datetime
import nested_admin


class IngredientAdmin(admin.ModelAdmin):
	exclude = ('ratio', )
	ordering = ['name']
	search_fields = ['name']
	list_display= ['name', 'price']

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

class CondimentAdmin(admin.ModelAdmin):
	search_fields = ['name']

class Program2CondimentInline(admin.TabularInline):
	model = Program2Condiment
	autocomplete_fields = ['condiment']
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
	fields = ('name', 'superprogram', 'date', ('condiments_price', 'condiments_bool'))
	inlines = [
		Program2DishInline, 
		Program2CongeeSoupInline, 
		Program2StapleInline,
		Program2CondimentInline,
		Program2OilInline, 
		Program2DisposableInline,
	]
	actions = ['duplicate_project']

	def duplicate_project(modeladmin, request, queryset):
		for project in queryset:
			project.pk = None
			project.date = datetime.date.today()
			project.save()
	duplicate_project.short_description = '复制所选的项目'

class SuperProgramAdmin(admin.ModelAdmin):
	pass

class CKProjectLocationAdmin(admin.ModelAdmin):
	search_fields = ['name']

class CKProject2SDish2StandardCountInline(nested_admin.NestedTabularInline):
	autocomplete_fields = ['location']
	model = CKProject2SDish2StandardCount
	extra = 1

class SDish2StandardIngredientInline(nested_admin.NestedTabularInline):
	model = SDish2StandardIngredient
	autocomplete_fields = ['ingredient']
	extra = 1

class SDish2StandardInline(nested_admin.NestedStackedInline):
	model = SDish2Standard
	inlines = [SDish2StandardIngredientInline]
	extra = 1

class SDishAdmin(nested_admin.NestedModelAdmin):
	inlines = [SDish2StandardInline]

class SDish2StandardAdmin(admin.ModelAdmin):
	search_fields = ['dish__name', 'standard']

	def has_module_permission(self, request):
		return False

def ckProject2SDish2StandardFormFactory(meal):

	class CKProject2SDish2StandardForm(ModelForm):

		class Meta:
			model = CKProject2SDish2Standard
			fields = '__all__'
			#exclude = ('meal', )

		def __init__(self, *args, **kwargs):
			if 'initial' not in kwargs:
				kwargs['initial'] = {}
			kwargs['initial'].update({'meal': meal})
			super(CKProject2SDish2StandardForm, self).__init__(*args, **kwargs)
			#self.fields['meal'].initial = meal

	return CKProject2SDish2StandardForm

class CKProject2SDish2StandardBreakfastInline(nested_admin.NestedStackedInline):
	model = CKProject2SDish2Standard
	form = ckProject2SDish2StandardFormFactory(Meal.BREAKFAST)
	#exclude = ('meal', )
	autocomplete_fields = ['sdish2standard']
	inlines = [CKProject2SDish2StandardCountInline]
	verbose_name = '早餐'
	verbose_name_plural = '早餐'
	extra = 1

	def get_queryset(self, request):
		return super().get_queryset(request).filter(meal=Meal.BREAKFAST)

class CKProject2SDish2StandardLunchInline(nested_admin.NestedStackedInline):
	model = CKProject2SDish2Standard
	form = ckProject2SDish2StandardFormFactory(Meal.LUNCH)
	#exclude = ('meal', )
	autocomplete_fields = ['sdish2standard']
	inlines = [CKProject2SDish2StandardCountInline]
	verbose_name = '午餐'
	verbose_name_plural = '午餐'
	extra = 1

	def get_queryset(self, request):
		return super().get_queryset(request).filter(meal=Meal.LUNCH)

class CKProject2SDish2StandardDinnerInline(nested_admin.NestedStackedInline):
	model = CKProject2SDish2Standard
	form = ckProject2SDish2StandardFormFactory(Meal.DINNER)
	#exclude = ('meal', )
	autocomplete_fields = ['sdish2standard']
	inlines = [CKProject2SDish2StandardCountInline]
	verbose_name = '晚餐'
	verbose_name_plural = '晚餐'
	extra = 1

	def get_queryset(self, request):
		return super().get_queryset(request).filter(meal=Meal.DINNER)

class CKProject2SDish2StandardMidnightInline(nested_admin.NestedStackedInline):
	model = CKProject2SDish2Standard
	form = ckProject2SDish2StandardFormFactory(Meal.MIDNIGHT)
	#exclude = ('meal', )
	autocomplete_fields = ['sdish2standard']
	inlines = [CKProject2SDish2StandardCountInline]
	verbose_name = '夜餐'
	verbose_name_plural = '夜餐'
	extra = 1

	def get_queryset(self, request):
		return super().get_queryset(request).filter(meal=Meal.MIDNIGHT)

class CKProjectAdmin(nested_admin.NestedModelAdmin):
	inlines = [CKProject2SDish2StandardBreakfastInline, 
		CKProject2SDish2StandardLunchInline,
		CKProject2SDish2StandardDinnerInline,
		CKProject2SDish2StandardMidnightInline
	]




admin.site.register(Ingredient, IngredientAdmin)
#admin.site.register(Dish, DishAdmin)
#admin.site.register(CongeeSoup, CongeeSoupAdmin)
#admin.site.register(Staple, StapleAdmin)
#admin.site.register(Condiment, CondimentAdmin)
#admin.site.register(Oil, OilAdmin)
#admin.site.register(Disposable, DisposableAdmin)
#admin.site.register(Program, ProgramAdmin)
#admin.site.register(SuperProgram, SuperProgramAdmin)

admin.site.register(CKProjectLocation, CKProjectLocationAdmin)
admin.site.register(CKProject, CKProjectAdmin)
admin.site.register(SDish, SDishAdmin)
admin.site.register(SDish2Standard, SDish2StandardAdmin)
