from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

import nested_admin
import guardian.admin as guardian_admin
from guardian.shortcuts import get_objects_for_user

from common.models import (
    Ingredient,
    IngredientPrice,
    Project,
    SDish,
    SDish2Standard,
    SDish2StandardIngredient
)


class IngredientPriceInlineFormset(BaseInlineFormSet):

    def clean(self):
        """Check that at least one price has been entered."""
        super().clean()
        if any(self.errors):
            return
        if not any(cleaned_data and not cleaned_data.get('DELETE', False)
                   for cleaned_data in self.cleaned_data):
            raise ValidationError('至少需要提供一个价格。')


class IngredientPriceInline(admin.TabularInline):
    model = IngredientPrice
    formset = IngredientPriceInlineFormset
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    admin_priority = 1
    exclude = ('ratio',)
    ordering = ['name']
    search_fields = ['name']
    inlines = [IngredientPriceInline]
    list_display = ['name_and_spec', 'latest_price_per_unit', 'category']
    list_filter = ['category']

    class Media:
        css = {"all": ("css/hide_admin_original.css",)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Enables autocomplete choices
        # to pre-filter based on category
        if 'category' in request.GET:
            qs = qs.filter(category=request.GET['category'])
        return qs


@admin.register(SDish)
class SDishAdmin(nested_admin.NestedModelAdmin):

    def sdish_inline():
        class SDish2StandardIngredientInline(nested_admin.NestedTabularInline):
            model = SDish2StandardIngredient
            autocomplete_fields = ['ingredient']
            extra = 1

        class SDish2StandardInline(nested_admin.NestedStackedInline):
            model = SDish2Standard
            inlines = [SDish2StandardIngredientInline]
            extra = 1

        return SDish2StandardInline

    admin_priority = 3
    inlines = [sdish_inline()]


@admin.register(SDish2Standard)
class SDish2StandardAdmin(admin.ModelAdmin):
    search_fields = ['dish__name', 'standard']

    def has_module_permission(self, request):
        return False


@admin.register(Project)
class ProjectAdmin(guardian_admin.GuardedModelAdmin):
    admin_priority = 2
    search_fields = ['name']

    def has_view_permission(self, request, obj=None):
        """
        Returns a boolean indicating whether a user has the view permission of the model.

        Note that here we check both the global view permission and object-level view permission.
        We add the object-level permission check to make the autocomplete feature work, since
        AutocompleteJsonView requires has_view_permission to return true so that it does not throw
        a PermissionDenied exception.
        """
        return (
            request.user.is_active and (
                super().has_view_permission(request, obj) or
                self.get_queryset(request).exists()
            )
        )

    def has_module_permission(self, request):
        """
        Returns a boolean indicating whether a user can see the model on the index page.

        A user can see the model on the index page if it is a superuser, or it has any one of
        the *global* view|add|change|delete permissions assigned to it. Note that we use the
        implementation of has_view_permission from the parent class to check the global view
        permission, since the implementation of the current class checks both the global view
        permission and the object-level view permission.
        """
        return (
            request.user.is_active and (
                request.user.is_superuser or
                super().has_view_permission(request) or
                self.has_add_permission(request) or
                self.has_change_permission(request) or
                self.has_delete_permission(request)
               )
        )

    def get_queryset(self, request):
        return get_objects_for_user(
            user=request.user,
            perms='view_project',
            klass=self.model,
            accept_global_perms=False
        )
