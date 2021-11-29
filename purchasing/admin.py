from collections import defaultdict
from copy import copy

from django.contrib import admin, messages
from django.contrib.admin.widgets import AutocompleteSelect
from django.forms import ModelForm
from django.http import HttpResponse
from django.utils.http import urlencode

import openpyxl

from common.admin import ProjectAdmin
from common.models import IngredientCategory, Project
from models import (
    ProjectPurchaseOrder,
    ProjectPurchaseOrderItem,
    PurchaseOrderSummary,
    PurchaseOrderSummaryItem
)
from common.views import rfc5987_content_disposition
from views import download_purchase_order_summary


def purchase_order_inline(model_class, category, extra_item=3, max_item=None):
    class AutoCompleteSelectWithCategory(AutocompleteSelect):
        def get_url(self):
            url = super().get_url()
            url += '?' + urlencode({
                'category': category.value
            })
            return url

    class ProjectPurchaseOrderItemForm(ModelForm):
        class Meta:
            fields = '__all__'
            widgets = {
                'ingredient': AutoCompleteSelectWithCategory(
                    ProjectPurchaseOrderItem._meta.get_field('ingredient'),
                    admin.site
                )
            }

    class ProjectPurchaseOrderItemInline(admin.TabularInline):
        model = model_class
        form = ProjectPurchaseOrderItemForm
        verbose_name = category.label
        verbose_name_plural = category.label
        extra = extra_item
        max_num = max_item
        autocomplete_fields = ['ingredient']

        def get_queryset(self, request):
            return super().get_queryset(request).filter(
                ingredient__category=category
            )

        # def formfield_for_foreignkey(self, db_field, request, **kwargs):
        #     if db_field.name == "ingredient":
        #         kwargs["queryset"] = Ingredient.objects.filter(category=category)
        #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

    return ProjectPurchaseOrderItemInline


@admin.register(ProjectPurchaseOrder)
class ProjectPurchaseOrderAdmin(admin.ModelAdmin):
    inlines = [
        purchase_order_inline(ProjectPurchaseOrderItem, category, 2)
        for category in IngredientCategory
    ]
    autocomplete_fields = ['project']

    class Media:
        css = {"all": ("css/hide_admin_original.css",)}

    @staticmethod
    def find_existing_match(existing_items, item):
        for existing_item in existing_items:
            if item.ingredient == existing_item.ingredient:
                return existing_item
        return None

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        try:
            PurchaseOrderSummary.objects.get(date=obj.date)
        except PurchaseOrderSummary.DoesNotExist:
            PurchaseOrderSummary.objects.create(date=obj.date)

    def delete_model(self, request, obj):
        date = copy(obj.date)
        super().delete_model(request, obj)

        orders = ProjectPurchaseOrder.objects.filter(date=date)
        if len(orders) == 0:
            try:
                summary = PurchaseOrderSummary.objects.get(date=date)
                summary.delete()
            except PurchaseOrderSummary.DoesNotExist:
                pass

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_model(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser or self.has_view_permission(request):
            return qs

        permitted_projects = ProjectAdmin(Project, self.admin_site).get_queryset(request)
        return qs.filter(project__in=permitted_projects)


@admin.register(PurchaseOrderSummary)
class PurchaseOrderSummaryAdmin(admin.ModelAdmin):
    inlines = [
        purchase_order_inline(PurchaseOrderSummaryItem, category, 0, 0)
        for category
        in IngredientCategory
    ]
    actions = ['download_purchase_order_summary']

    class Media:
        css = {"all": ("css/hide_admin_original.css",)}

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        # Recalculate the summary
        summary = PurchaseOrderSummary.objects.get(id=object_id)
        PurchaseOrderSummaryItem.objects.filter(summary=summary).delete()

        items = ProjectPurchaseOrderItem.objects.filter(order__date=summary.date)
        ingredient_quantities = defaultdict(float)
        for item in items:
            ingredient_quantities[item.ingredient] += item.quantity
        for ingredient, quantity in ingredient_quantities.items():
            PurchaseOrderSummaryItem.objects.create(
                summary=summary,
                ingredient=ingredient,
                quantity=quantity
            )
        summary.save()

        return super().changeform_view(request, object_id, form_url, extra_context)

    @admin.action(description='下载采购清单汇总')
    def download_purchase_order_summary(self, request, queryset):
        if len(queryset) > 1:
            self.message_user(request, '只能选择一个日期', level=messages.ERROR)

        date = queryset[0].date
        wb = download_purchase_order_summary(date)
        response = HttpResponse(
            content=openpyxl.writer.excel.save_virtual_workbook(wb),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename = '采购清单%d月%d日.xlsx' % (date.month, date.day)
        response['Content-Disposition'] = rfc5987_content_disposition(filename)
        return response
