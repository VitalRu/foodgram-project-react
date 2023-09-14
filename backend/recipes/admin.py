from django.contrib import admin

from .models import Recipe, Ingredient, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'display_tags',
                    'display_ingredients', 'text', 'cooking_time', 'pub_date')

    list_filter = ('name', 'author', 'tags')

    search_fields = ('name', r'^author__username', r'^tags__name',
                     r'^tags__slug')
    empty_value_display = '-пусто-'

    def display_tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])

    def display_ingredients(self, obj):
        return ', '.join(
            [ingredient.name for ingredient in obj.ingredients.all()]
        )

    display_tags.short_description = 'tags'
    display_ingredients.short_description = 'ingredients'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('id', r'^name')
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('name',)
