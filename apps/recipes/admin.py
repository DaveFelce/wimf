from django.contrib import admin

from apps.recipes.models import Recipe


class RecipeAdmin(admin.ModelAdmin):
    fields = ["name", "ingredients", "url"]
    search_fields = ['ingredients']
    ordering = ['name']


admin.site.register(Recipe, RecipeAdmin)
