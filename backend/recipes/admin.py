from django.contrib import admin

from .models import FavoriteRecipe, Ingredient, Recipe, ShoppingList, Tag, IngredientsInRecipe, TagsInRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'display_tags',
                    'display_ingredients', 'text', 'cooking_time', 'pub_date',
                    'favorite_count')

    list_filter = ('name', 'author', 'tags')

    search_fields = ('name', r'^author__username', r'^tags__name',
                     r'^tags__slug')

    def display_tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])

    def display_ingredients(self, obj):
        return ', '.join(
            [ingredient.name for ingredient in obj.ingredients.all()]
        )

    def favorite_count(self, obj):
        return obj.favorite_recipe.count()

    display_tags.short_description = 'tags'
    display_ingredients.short_description = 'ingredients'
    favorite_count.short_description = 'favorite'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('id', r'^name')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('name',)


@admin.register(IngredientsInRecipe)
class IngredientsInRecipeAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount',)
    search_fields = (r'^ingredient__name', r'^recipe__name',)
    list_filter = ('recipe__name',)


@admin.register(TagsInRecipe)
class TagsInRecipeAdmin(admin.ModelAdmin):
    list_display = ('tag', 'recipe')
    search_fields = (r'^tag__name', r'^recipe__name',)
    list_filter = ('recipe__name',)


@admin.register(FavoriteRecipe)
class FavoriteRecipe(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(ShoppingList)
class ShoppingList(admin.ModelAdmin):
    list_display = ('user', 'recipe')
