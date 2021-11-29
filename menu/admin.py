from copy import copy
from datetime import date

import django.forms as forms
from django.contrib import admin, messages

from django.http import HttpResponse
from django.shortcuts import render

import nested_admin
import openpyxl

from models import (
    CKProject,
    CKProjectLocation,
    CKProject2SDish2Standard,
    CKProject2SDish2StandardCount,
    Meal
)
from common.views import rfc5987_content_disposition
from views.ck_reports import generate_ckproject_weekly_report


@admin.register(CKProjectLocation)
class CKProjectLocationAdmin(admin.ModelAdmin):
    search_fields = ['name']


def ckproject_inline(meal):
    class CKProject2SDish2StandardCountInline(nested_admin.NestedTabularInline):
        autocomplete_fields = ['location']
        model = CKProject2SDish2StandardCount
        extra = 0

    class CKProject2SDish2StandardForm(forms.ModelForm):
        class Meta:
            model = CKProject2SDish2Standard
            exclude = ['meal']

        def save(self, commit=True):
            self.instance.meal = meal
            return super().save(commit)

    class CKProject2SDish2StandardInline(nested_admin.NestedStackedInline):
        model = CKProject2SDish2Standard
        form = CKProject2SDish2StandardForm
        autocomplete_fields = ['sdish2standard']
        inlines = [CKProject2SDish2StandardCountInline]
        verbose_name = meal.label
        verbose_name_plural = meal.label
        extra = 0

        def get_formset(self, request, obj=None, **kwargs):
            formset = super().get_formset(request, obj, **kwargs)
            sdish2standard = formset.form.base_fields['sdish2standard']
            sdish2standard.widget.can_add_related = False
            sdish2standard.widget.can_change_related = False
            sdish2standard.widget.can_delete_related = False
            return formset

        def get_queryset(self, request):
            return super().get_queryset(request).filter(meal=meal)

    return CKProject2SDish2StandardInline


@admin.register(CKProject)
class CKProjectAdmin(nested_admin.NestedModelAdmin):
    autocomplete_fields = ['project']
    inlines = [ckproject_inline(meal) for meal in Meal]
    actions = ['duplicate_project', 'generate_weekly_report']

    class Media:
        css = {"all": ("css/hide_admin_original.css",)}

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
            project_copy = copy(project)
            project_copy.pk = None
            form_date_key = 'form-' + str(index) + '-date'
            project_copy.date = request.POST.get(form_date_key, date.today())

            # This save is required for the following m2m copy
            project_copy.save()

            p2ds = CKProject2SDish2Standard.objects.filter(project=project)
            for p2d in p2ds:
                p2d_copy = CKProject2SDish2Standard(
                    project=project_copy,
                    sdish2standard=p2d.sdish2standard,
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
