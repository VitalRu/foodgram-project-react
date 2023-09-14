from django.contrib import admin

from .models import Recipe, Ingredient, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'image', 'tags', 'ingredients',
                    'text', 'cooking_time', 'pub_date')
    list_filter = ('name', 'author', 'tags')
    search_fields = (r'^name', r'^author', 'tags')
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author', 'measurement_unit')
    search_fields = ('id', r'^name')
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('name',)
