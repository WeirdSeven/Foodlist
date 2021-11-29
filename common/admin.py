from django.contrib import admin

import nested_admin
import guardian.admin as guardian_admin
from guardian.shortcuts import get_objects_for_user

from models import Ingredient, Project, SDish, SDish2Standard, SDish2StandardIngredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    exclude = ('ratio',)
    ordering = ['name']
    search_fields = ['name']
    list_display = ['name', 'category', 'price']
    list_filter = ['category']

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Enables autocomplete choices
        # to pre-filter based on category
        if 'category' in request.GET:
            qs = qs.filter(category=request.GET['category'])
        return qs


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


@admin.register(SDish)
class SDishAdmin(nested_admin.NestedModelAdmin):
    inlines = [sdish_inline()]


@admin.register(SDish2Standard)
class SDish2StandardAdmin(admin.ModelAdmin):
    search_fields = ['dish__name', 'standard']

    def has_module_permission(self, request):
        return False


@admin.register(Project)
class ProjectAdmin(guardian_admin.GuardedModelAdmin):
    search_fields = ['name']

    def has_view_permission(self, request, obj=None):
        """
        Returns a boolean indicating whether a user has the view permission of the model.

        Note that here we check both the global view permission and object-level view permission.
        We add the object-level permission check to make the autocomplete feature work, since
        AutocompleteJsonView requires has_view_permission to return true so that it does not throw
        a PermissionDnied exception.
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
