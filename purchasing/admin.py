from collections import defaultdict
from copy import copy
from datetime import date
from urllib.parse import quote as urlquote

from django.contrib import admin, messages
from django.contrib.admin.exceptions import DisallowedModelAdminToField
from django.contrib.admin.options import IS_POPUP_VAR, TO_FIELD_VAR
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.utils import quote, unquote, flatten_fieldsets
from django.contrib.admin import helpers, widgets
from django.core.exceptions import PermissionDenied
from django.forms import formset_factory, DateField, Form, ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import gettext as _

import openpyxl

from common.admin import ProjectAdmin
from common.models import IngredientCategory, Project, RequestStatus
from common.views import rfc5987_content_disposition
from purchasing.models import (
    ProjectSettings,
    ProjectPurchaseOrder,
    ProjectPurchaseOrderItem,
    PurchaseOrderSummary,
    PurchaseOrderSummaryItem
)
from purchasing.views import download_project_purchase_order, download_purchase_order_summary


@admin.register(ProjectSettings)
class ProjectSettingsAdmin(admin.ModelAdmin):
    admin_priority = 0
    autocomplete_fields = ['project']

    def get_exclude(self, request, obj=None):
        exclude = list(super().get_exclude(request, obj) or [])

        if request.user.is_superuser:
            return exclude

        exclude.append('project')
        return exclude


def purchase_order_inline(model_class, category, extra_item=3, max_item=None):
    class AutoCompleteSelectWithCategory(widgets.AutocompleteSelect):
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

    return ProjectPurchaseOrderItemInline


@admin.register(ProjectPurchaseOrder)
class ProjectPurchaseOrderAdmin(admin.ModelAdmin):
    admin_priority = 1
    exclude = ['status']
    inlines = [
        purchase_order_inline(ProjectPurchaseOrderItem, category, 2)
        for category in IngredientCategory
    ]
    autocomplete_fields = ['project']
    list_display = ['project', 'date', 'emoji_and_status']
    actions = ['duplicate_project_purchase_order', 'download_project_purchase_order']

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

    def has_global_view_permission(self, request):
        """
        Checks to see whether the user is granted the global
        view_projectpurchaseorder permission.
        """
        opts = self.opts
        codename_view = '%s_%s' % ('view', opts.model_name)
        return request.user.has_perm('%s.%s' % (opts.app_label, codename_view))

    def has_object_view_permission(self, request, obj):
        """
        Whether a user can view a project purchase order depends on
        whether the user can view the project.
        """
        project = getattr(obj, 'project', None)
        return request.user.has_perm('common.view_project', project)

    def has_view_permission(self, request, obj=None):
        """
        This method combines the global and object-level view permissions.
        """
        return (self.has_global_view_permission(request) or
                self.has_object_view_permission(request, obj))

    def has_change_permission(self, request, obj=None):
        """
        A regular user can no longer change an order
        after it has been submitted.
        """
        has_change_permission = super().has_change_permission(request, obj)
        if request.user.is_superuser or not obj:
            return has_change_permission

        return has_change_permission and obj.status == RequestStatus.EDITING

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser or self.has_global_view_permission(request):
            return qs

        permitted_projects = ProjectAdmin(Project, self.admin_site).get_queryset(request)
        return qs.filter(project__in=permitted_projects)

    def send_sms_notification(self):
        pass

    def submit_model(self, request, obj):
        obj.status = RequestStatus.SUBMITTED
        obj.save()

        self.send_sms_notification()

    def response_submit(self, request, opts, preserved_filters, msg_dict):
        msg = format_html('成功提交了 {name} “{obj}”。', **msg_dict)
        self.message_user(request, msg, messages.SUCCESS)
        if self.has_view_or_change_permission(request):
            post_url = reverse('admin:%s_%s_changelist' %
                               (opts.app_label, opts.model_name),
                               current_app=self.admin_site.name)
            post_url = add_preserved_filters(
                {'preserved_filters': preserved_filters, 'opts': opts}, post_url)
        else:
            post_url = reverse('admin:index', current_app=self.admin_site.name)
        return HttpResponseRedirect(post_url)

    def response_add(self, request, obj, post_url_continue=None):
        opts = obj._meta
        preserved_filters = self.get_preserved_filters(request)

        # Add a link to the object's change form if the user can edit the obj.
        if self.has_change_permission(request, obj):
            obj_url = reverse(
                'admin:%s_%s_change' % (opts.app_label, opts.model_name),
                args=(quote(obj.pk),),
                current_app=self.admin_site.name,
            )
            obj_repr = format_html('<a href="{}">{}</a>', urlquote(obj_url), obj)
        else:
            obj_repr = str(obj)
        msg_dict = {
            'name': opts.verbose_name,
            'obj': obj_repr,
        }

        if "_submit" in request.POST:
            self.submit_model(request, obj)
            return self.response_submit(request, opts, preserved_filters, msg_dict)
        else:
            return super().response_change(request, obj)

    def response_change(self, request, obj):
        opts = self.model._meta
        preserved_filters = self.get_preserved_filters(request)

        msg_dict = {
            'name': opts.verbose_name,
            'obj': format_html('<a href="{}">{}</a>', urlquote(request.path), obj),
        }

        if "_submit" in request.POST:
            self.submit_model(request, obj)
            return self.response_submit(request, opts, preserved_filters, msg_dict)
        else:
            return super().response_change(request, obj)

    @staticmethod
    def all_valid(parent_form, formsets):
        if not all([formset.is_valid() for formset in formsets]):
            return False

        def get_order(formsets):
            for formset in formsets:
                for form in formset.forms:
                    data = form.cleaned_data
                    if data and not data['DELETE']:
                        return data['order']

        order = get_order(formsets)
        # No order will be found only if there are no valid inline items.
        if not order:
            return True

        total_cost = 0
        for formset in formsets:
            for form in formset.forms:
                data = form.cleaned_data
                # The inline has been emptied or to be deleted
                if not data or data['DELETE']:
                    continue

                total_cost += data['ingredient'].effective_price(order.date) * data['quantity']

        budget = order.project.purchasing_settings.daily_purchasing_budget
        overbudget = total_cost - budget
        if overbudget <= 0:
            return True
        else:
            error_msg = f'成本{total_cost}元。预算{budget}元。超支{overbudget}元。'
            parent_form.add_error(None, error_msg)
            return False

    def _changeform_view(self, request, object_id, form_url, extra_context):
        """
        I know overriding such a long method is terrible! But I do not know what a better
        approach would be. I will take a look at this patch method to try to patch all_valid().
        https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch
        """
        to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField("The field %s cannot be referenced." % to_field)

        model = self.model
        opts = model._meta

        if request.method == 'POST' and '_saveasnew' in request.POST:
            object_id = None

        add = object_id is None

        if add:
            if not self.has_add_permission(request):
                raise PermissionDenied
            obj = None

        else:
            obj = self.get_object(request, unquote(object_id), to_field)

            if request.method == 'POST':
                if not self.has_change_permission(request, obj):
                    raise PermissionDenied
            else:
                if not self.has_view_or_change_permission(request, obj):
                    raise PermissionDenied

            if obj is None:
                return self._get_obj_does_not_exist_redirect(request, opts, object_id)

        fieldsets = self.get_fieldsets(request, obj)
        ModelForm = self.get_form(
            request, obj, change=not add, fields=flatten_fieldsets(fieldsets)
        )
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=obj)
            form_validated = form.is_valid()
            if form_validated:
                new_object = self.save_form(request, form, change=not add)
            else:
                new_object = form.instance
            formsets, inline_instances = self._create_formsets(request, new_object, change=not add)
            if self.all_valid(form, formsets) and form_validated:
                self.save_model(request, new_object, form, not add)
                self.save_related(request, form, formsets, not add)
                change_message = self.construct_change_message(request, form, formsets, add)
                if add:
                    self.log_addition(request, new_object, change_message)
                    return self.response_add(request, new_object)
                else:
                    self.log_change(request, new_object, change_message)
                    return self.response_change(request, new_object)
            else:
                form_validated = False
        else:
            if add:
                initial = self.get_changeform_initial_data(request)
                form = ModelForm(initial=initial)
                formsets, inline_instances = self._create_formsets(request, form.instance, change=False)
            else:
                form = ModelForm(instance=obj)
                formsets, inline_instances = self._create_formsets(request, obj, change=True)

        if not add and not self.has_change_permission(request, obj):
            readonly_fields = flatten_fieldsets(fieldsets)
        else:
            readonly_fields = self.get_readonly_fields(request, obj)
        adminForm = helpers.AdminForm(
            form,
            list(fieldsets),
            # Clear prepopulated fields on a view-only form to avoid a crash.
            self.get_prepopulated_fields(request, obj) if add or self.has_change_permission(request, obj) else {},
            readonly_fields,
            model_admin=self)
        media = self.media + adminForm.media

        inline_formsets = self.get_inline_formsets(request, formsets, inline_instances, obj)
        for inline_formset in inline_formsets:
            media = media + inline_formset.media

        if add:
            title = _('Add %s')
        elif self.has_change_permission(request, obj):
            title = _('Change %s')
        else:
            title = _('View %s')
        context = {
            **self.admin_site.each_context(request),
            'title': title % opts.verbose_name,
            'subtitle': str(obj) if obj else None,
            'adminform': adminForm,
            'object_id': object_id,
            'original': obj,
            'is_popup': IS_POPUP_VAR in request.POST or IS_POPUP_VAR in request.GET,
            'to_field': to_field,
            'media': media,
            'inline_admin_formsets': inline_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'preserved_filters': self.get_preserved_filters(request),
        }

        # Hide the "Save" and "Save and continue" buttons if "Save as New" was
        # previously chosen to prevent the interface from getting confusing.
        if request.method == 'POST' and not form_validated and "_saveasnew" in request.POST:
            context['show_save'] = False
            context['show_save_and_continue'] = False
            # Use the change template instead of the add template.
            add = False

        context.update(extra_context or {})

        return self.render_change_form(request, context, add=add, change=not add, obj=obj, form_url=form_url)

    @admin.action(description='复制所选的项目采购清单')
    def duplicate_project_purchase_order(self, request, queryset):

        queryset = queryset.order_by('project__name', 'date')

        class ProjectPurchaseOrderDateForm(Form):
            date = DateField(
                label='更改后日期',
                widget=admin.widgets.AdminDateWidget()
            )

        if not request.POST.get('post'):
            return render(request, 'purchasing/purchase_order_duplicate_date.html', {
                'queryset': queryset,
                'formset': formset_factory(ProjectPurchaseOrderDateForm, extra=queryset.count())(),
                'title': '选择日期',
                # For styles
                **self.admin_site.each_context(request),
                'opts': self.model._meta,
                'media': self.media
            })

        for index, order in enumerate(queryset):
            order_copy = ProjectPurchaseOrder(
                project=order.project,
                date=request.POST.get(f'form-{index}-date', date.today())
            )

            # This save is required for the following m2m copy
            order_copy.save()

            for item in order.items.all():
                ProjectPurchaseOrderItem.objects.create(
                    order=order_copy,
                    ingredient=item.ingredient,
                    quantity=item.quantity
                )

            order_copy.save()

    @admin.action(description='下载所选的项目采购清单')
    def download_project_purchase_order(self, request, queryset):
        if len(queryset) > 1:
            self.message_user(request, '只能选择一个采购清单', level=messages.ERROR)

        order = queryset[0]
        wb = download_project_purchase_order(order)
        response = HttpResponse(
            content=openpyxl.writer.excel.save_virtual_workbook(wb),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename = f'项目采购清单 {order}.xlsx'
        response['Content-Disposition'] = rfc5987_content_disposition(filename)
        return response


@admin.register(PurchaseOrderSummary)
class PurchaseOrderSummaryAdmin(admin.ModelAdmin):
    admin_priority = 2
    inlines = [
        purchase_order_inline(PurchaseOrderSummaryItem, category, 0, 0)
        for category
        in IngredientCategory
    ]
    actions = ['download_purchase_order_summary']

    class Media:
        css = {"all": ("css/hide_admin_original.css",)}

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
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

        summary_date = queryset[0].date
        wb = download_purchase_order_summary(summary_date)
        response = HttpResponse(
            content=openpyxl.writer.excel.save_virtual_workbook(wb),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename = f'采购清单汇总 {summary_date}.xlsx'
        response['Content-Disposition'] = rfc5987_content_disposition(filename)
        return response
