from django_filters import rest_framework as filters

from recipes.models import Recipe, Ingredient


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.CharFilter(
        field_name='author__username', lookup_expr='icontains'
    )
    ingredients = filters.AllValuesMultipleFilter(
        field_name='ingredients__name', lookup_expr='icontains'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'ingredients')


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith',)

    class Meta:
        model = Ingredient
        fields = ('name',)
