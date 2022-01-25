from django.contrib import admin, messages
from django.contrib.admin.widgets import AutocompleteSelect
from django.forms import ModelForm
from django.utils.http import urlencode

from common.admin import ProjectAdmin
from common.models import IngredientCategory, Project
from inventory.models import InventoryInList, InventoryInListItem, RequestStatus


def inventory_list_item_inline(model_class, category, extra_item=3, max_item=None):
    class AutoCompleteSelectWithCategory(AutocompleteSelect):
        def get_url(self):
            url = super().get_url()
            url += '?' + urlencode({
                'category': category.value
            })
            return url

    class InventoryListItemForm(ModelForm):
        class Meta:
            fields = '__all__'
            widgets = {
                'ingredient': AutoCompleteSelectWithCategory(
                    model_class._meta.get_field('ingredient'),
                    admin.site
                )
            }

    class InventoryListItemFormInline(admin.TabularInline):
        model = model_class
        form = InventoryListItemForm
        verbose_name = category.label
        verbose_name_plural = category.label
        extra = extra_item
        max_num = max_item
        autocomplete_fields = ['ingredient']

        def get_queryset(self, request):
            return super().get_queryset(request).filter(
                ingredient__category=category
            )

    return InventoryListItemFormInline


@admin.register(InventoryInList)
class InventoryInListAdmin(admin.ModelAdmin):
    inlines = [
        inventory_list_item_inline(InventoryInListItem, IngredientCategory.CONDIMENT),
        inventory_list_item_inline(InventoryInListItem, IngredientCategory.DRY),
        inventory_list_item_inline(InventoryInListItem, IngredientCategory.RICE_NOODLE_OIL),
        inventory_list_item_inline(InventoryInListItem, IngredientCategory.DISPOSABLE)
    ]
    autocomplete_fields = ['project']
    list_display = ['project', 'date', 'emoji_and_status']

    class Media:
        css = {"all": ("css/hide_admin_original.css",)}

    def can_edit_comments(self, request):
        return request.user.has_perm('%s.%s' % (self.opts.app_label, 'edit_comments'))

    def can_edit_project_date_and_items(self, request):
        opts = self.opts
        codename = '%s_%s' % ('add', opts.model_name)
        return request.user.has_perm('%s.%s' % (opts.app_label, codename))

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj) or [])

        if request.user.is_superuser or not obj:
            return readonly_fields

        # if obj.status in [
        #     RequestStatus.APPROVED,
        #     RequestStatus.REJECTED,
        #     RequestStatus.REEDITING
        # ]:
        #     readonly_fields.append('comments')

        if not self.can_edit_comments(request):
            readonly_fields.append('comments')

        if not self.can_edit_project_date_and_items(request):
            readonly_fields.extend(['project', 'date'])

        return readonly_fields

    def get_exclude(self, request, obj=None):
        exclude = list(super().get_exclude(request, obj) or [])

        if request.user.is_superuser:
            return exclude

        # exclude.append('status')

        # The visibility of comments depends on
        # both status and the edit_comments permission
        if not obj:
            exclude.append('comments')
        elif obj.status == RequestStatus.EDITING:
            exclude.append('comments')
        elif obj.status in [RequestStatus.SUBMITTED, RequestStatus.RESUBMITTED]:
            if not self.can_edit_comments(request):
                exclude.append('comments')

        return exclude

    def has_change_permission(self, request, obj=None):
        has_change_permission = super().has_change_permission(request, obj)
        if request.user.is_superuser or not obj:
            return has_change_permission

        # When inventory managers can edit
        if obj.status in [
            RequestStatus.EDITING,
            RequestStatus.REEDITING,
            RequestStatus.REJECTED
        ] and has_change_permission and self.can_edit_project_date_and_items(request):
            return True

        # When project managers can edit
        if obj.status in [
            RequestStatus.SUBMITTED,
            RequestStatus.RESUBMITTED
        ] and has_change_permission and self.can_edit_comments(request):
            return True

        return False

    def get_queryset(self, request):
        """
        If a user has global view permission for InventoryInList, they can see
        all inventory-in list of all projects.
        If a user does not have global view permission for InventoryInList, they
        can only see inventory-in lists of projects for which they have the view permission.
        """
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        permitted_projects = ProjectAdmin(Project, self.admin_site).get_queryset(request)
        return qs.filter(project__in=permitted_projects)

