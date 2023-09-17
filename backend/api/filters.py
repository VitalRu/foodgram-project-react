from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.AllValuesFilter(field_name='author')
    ingredients = filters.AllValuesMultipleFilter(
        field_name='ingredients__name'
    )
    is_favorited = filters.BooleanFilter(method='get_favorited')
    is_in_shopping_cart = filters.BooleanFilter(method='get_in_shopping_cart')

    def get_in_shopping_cart(self, queryset, name, data):
        if data and not self.request.user.is_anonymous:
            return queryset.filter(
                in_shopping_list__user=self.request.user
            )
        return queryset

    def get_favorited(self, queryset, name, data):
        if data and not self.request.user.is_anonymous:
            return queryset.filter(favorite_recipe__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart')


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith',)

    class Meta:
        model = Ingredient
        fields = ('name',)
