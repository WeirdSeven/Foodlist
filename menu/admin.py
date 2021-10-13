import copy

import django.forms as forms
from django.contrib import admin, messages
from django.http import HttpResponse
from django.shortcuts import render

import nested_admin
import openpyxl

from .models import *
from .views.ck_reports import generate_ckproject_weekly_report
from .views.reportutils import rfc5987_content_disposition


class IngredientAdmin(admin.ModelAdmin):
    exclude = ('ratio',)
    ordering = ['name']
    search_fields = ['name']
    list_display = ['name', 'price']


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


def ckproject2dish2standard_formfactory(meal):
    class CKProject2SDish2StandardForm(forms.ModelForm):
        class Meta:
            model = CKProject2SDish2Standard
            fields = '__all__'
            # exclude = ('meal', )

        def __init__(self, *args, **kwargs):
            if 'initial' not in kwargs:
                kwargs['initial'] = {}
            kwargs['initial'].update({'meal': meal})
            super(CKProject2SDish2StandardForm, self).__init__(*args, **kwargs)
            # self.fields['meal'].initial = meal

    return CKProject2SDish2StandardForm


class CKProject2SDish2StandardBreakfastInline(nested_admin.NestedStackedInline):
    model = CKProject2SDish2Standard
    form = ckproject2dish2standard_formfactory(Meal.BREAKFAST)
    # exclude = ('meal', )
    autocomplete_fields = ['sdish2standard']
    inlines = [CKProject2SDish2StandardCountInline]
    verbose_name = '早餐'
    verbose_name_plural = '早餐'
    extra = 1

    def get_queryset(self, request):
        return super().get_queryset(request).filter(meal=Meal.BREAKFAST)


class CKProject2SDish2StandardLunchInline(nested_admin.NestedStackedInline):
    model = CKProject2SDish2Standard
    form = ckproject2dish2standard_formfactory(Meal.LUNCH)
    # exclude = ('meal', )
    autocomplete_fields = ['sdish2standard']
    inlines = [CKProject2SDish2StandardCountInline]
    verbose_name = '午餐'
    verbose_name_plural = '午餐'
    extra = 1

    def get_queryset(self, request):
        return super().get_queryset(request).filter(meal=Meal.LUNCH)


class CKProject2SDish2StandardDinnerInline(nested_admin.NestedStackedInline):
    model = CKProject2SDish2Standard
    form = ckproject2dish2standard_formfactory(Meal.DINNER)
    # exclude = ('meal', )
    autocomplete_fields = ['sdish2standard']
    inlines = [CKProject2SDish2StandardCountInline]
    verbose_name = '晚餐'
    verbose_name_plural = '晚餐'
    extra = 1

    def get_queryset(self, request):
        return super().get_queryset(request).filter(meal=Meal.DINNER)


class CKProject2SDish2StandardMidnightInline(nested_admin.NestedStackedInline):
    model = CKProject2SDish2Standard
    form = ckproject2dish2standard_formfactory(Meal.MIDNIGHT)
    # exclude = ('meal', )
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
    actions = ['duplicate_project', 'generate_weekly_report']

    @admin.action(description='复制所选的项目')
    def duplicate_project(self, request, queryset):

        queryset = queryset.order_by('name', 'date')

        class CKProjectDateForm(forms.Form):
            date = forms.DateField(
                label='更改后日期',
                widget=admin.widgets.AdminDateWidget()
            )

        if not request.POST.get('post'):
            print(queryset.count())
            return render(request, 'menu/ckproject_duplicate_date.html', {
                'queryset': queryset,
                'formset': forms.formset_factory(CKProjectDateForm, extra=queryset.count())(),
                'title': '选择日期',
                # For styles
                **self.admin_site.each_context(request),
                'opts': self.model._meta,
                'media': self.media
            })

        for index, project in enumerate(queryset):
            project_copy = copy.copy(project)
            project_copy.pk = None
            form_date_key = 'form-' + str(index) + '-date'
            project_copy.date = request.POST.get(form_date_key, datetime.date.today())

            # This save is required for the following m2m copy
            project_copy.save()

            for dish in project.sdishe2standards.all():
                p2d = CKProject2SDish2Standard.objects.get(
                    project__pk=project.pk,
                    sdish2standard__pk=dish.pk
                )
                p2d_copy = CKProject2SDish2Standard(
                    project=project_copy,
                    sdish2standard=dish,
                    meal=p2d.meal,
                    course=p2d.course
                )
                p2d_copy.save()

                p2dc_all = CKProject2SDish2StandardCount.objects.filter(project2dish2standard=p2d)
                for p2dc in p2dc_all:
                    CKProject2SDish2StandardCount.objects.create(
                        project2dish2standard=p2d_copy,
                        location=p2dc.location,
                        count=p2dc.count
                    )

            project_copy.save()

    @staticmethod
    def check_dates_same_week(dates):
        """ dates should go from Monday to Sunday """
        if len(dates) != 7:
            return False
        for i in range(7):
            if dates[i].weekday() != i:
                return False
        return True

    @admin.action(description='为所选项目生成周报告')
    def generate_weekly_report(self, request, queryset):
        project_names = queryset.values_list('name', flat=True).distinct()
        project_name_count = project_names.count()
        if project_name_count > 1:
            self.message_user(request, "只能为相同名称的项目生成报告", level=messages.ERROR)
            return

        dates = list(queryset.values_list('date', flat=True).order_by('date'))
        if not self.check_dates_same_week(dates):
            self.message_user(request, '所向项目的日期必须是周一到周日', level=messages.ERROR)

        wb = generate_ckproject_weekly_report(queryset.order_by('date'))
        response = HttpResponse(
            content=openpyxl.writer.excel.save_virtual_workbook(wb),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename = '%s菜单计划量%d月%d日.xlsx' % (project_names[0], dates[0].month, dates[0].day)
        response['Content-Disposition'] = rfc5987_content_disposition(filename)
        return response


admin.site.register(Ingredient, IngredientAdmin)
# admin.site.register(Dish, DishAdmin)
# admin.site.register(CongeeSoup, CongeeSoupAdmin)
# admin.site.register(Staple, StapleAdmin)
# admin.site.register(Condiment, CondimentAdmin)
# admin.site.register(Oil, OilAdmin)
# admin.site.register(Disposable, DisposableAdmin)
# admin.site.register(Program, ProgramAdmin)
# admin.site.register(SuperProgram, SuperProgramAdmin)

admin.site.register(CKProjectLocation, CKProjectLocationAdmin)
admin.site.register(CKProject, CKProjectAdmin)
admin.site.register(SDish, SDishAdmin)
admin.site.register(SDish2Standard, SDish2StandardAdmin)
